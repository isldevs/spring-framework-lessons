#!/usr/bin/env python3
"""Compile/run the actual DI demo and save raw, separated provenance evidence."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
E=ROOT.parent/'evidence';E.mkdir(exist_ok=True)
def run(cmd,name):
 p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
 (E/f'java-{name}.stdout.txt').write_text(p.stdout)
 (E/f'java-{name}.stderr.txt').write_text(p.stderr)
 (E/f'java-{name}.exit-code.txt').write_text(str(p.returncode)+'\n')
 (E/f'java-{name}.command.json').write_text(json.dumps({'command':cmd,'cwd':str(ROOT),'exit_code':p.returncode},indent=2)+'\n')
 if p.returncode:raise RuntimeError(f'{name} failed: {p.stderr}')
 return p
hashcheck=run(['sha256sum','-c','dependencies.sha256'],'dependencies')
(ROOT/'build').mkdir(exist_ok=True)
classpath=':'.join(str(p.relative_to(ROOT)) for p in sorted((ROOT/'lib').glob('*.jar')))
compile_result=run(['java','-jar','lib/ecj-3.40.0.jar','-17','-parameters','-warn:none','-cp',classpath,'-d','build',*[str(p.relative_to(ROOT)) for p in sorted((ROOT/'src/lesson/di').glob('*.java'))]],'compile')
program=run(['java','-cp','build:lib/*','lesson.di.DiDemo'],'program')
version=subprocess.run(['java','-version'],capture_output=True,text=True,check=True)
(E/'java-version.txt').write_text(version.stderr)
source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'src').rglob('*.java'))}
(E/'java-source-hashes.sha256').write_text(''.join(h+'  '+p+'\n' for p,h in source_hashes.items()))
result={'compile_exit_code':compile_result.returncode,'program_exit_code':program.returncode,'compile_stderr_empty':not compile_result.stderr,'program_stderr_empty':not program.stderr,'stdout_lines':program.stdout.splitlines(),'runtime':version.stderr.strip(),'spring_framework':'6.2.11','ecj':'3.40.0','class_file_target':'Java17','source_sha256':source_hashes,'dependency_hash_check_exit_code':hashcheck.returncode,'verified_assertions':['configured component definitions exist before singleton constructors','Repo constructed before OrderService receives it','OrderService wired before context ready/application use','single unannotated constructor used','injected Repo is same managed Repo bean','one unambiguous Repo candidate','default singleton lookup does not reconstruct graph','application reaches repository through injected service']}
(E/'java-verification-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(program.stdout,end='');print('Compilation/run/dependency hashes verified; raw evidence retained.')
