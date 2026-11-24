#!/usr/bin/env python3
"""Actual ECJ compilation, multiple-context JUnit tests and application execution."""
from pathlib import Path
import hashlib,json,subprocess,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent;E=ROOT.parent/'evidence';E.mkdir(exist_ok=True)
def run(cmd,stem):
 p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
 (E/f'java-{stem}.stdout.txt').write_text(p.stdout)
 (E/f'java-{stem}.stderr.txt').write_text(p.stderr)
 (E/f'java-{stem}.exit-code.txt').write_text(str(p.returncode)+'\n')
 (E/f'java-{stem}.command.json').write_text(json.dumps({'command':cmd,'cwd':str(ROOT),'exit_code':p.returncode},indent=2)+'\n')
 if p.returncode:raise RuntimeError(f'{stem} failed\n{p.stderr}\n{p.stdout}')
 return p
run(['sha256sum','-c','dependencies.sha256'],'dependencies')
cp=':'.join(str(p.relative_to(ROOT)) for p in sorted((ROOT/'lib').glob('*.jar')))
(ROOT/'build/main').mkdir(parents=True,exist_ok=True);(ROOT/'build/test').mkdir(parents=True,exist_ok=True);(ROOT/'build/test-results').mkdir(parents=True,exist_ok=True)
compiler=['java','-jar','lib/ecj-3.40.0.jar','-17','-parameters','-warn:none']
main=run([*compiler,'-cp',cp,'-d','build/main',*[str(p.relative_to(ROOT)) for p in sorted((ROOT/'src/main/java').rglob('*.java'))]],'compile-main')
tests=run([*compiler,'-cp','build/main:'+cp,'-d','build/test',*[str(p.relative_to(ROOT)) for p in sorted((ROOT/'src/test/java').rglob('*.java'))]],'compile-tests')
# Actual independent and parent-child AnnotationConfigApplicationContexts occur inside JUnit.
test=run(['java','-cp','build/main:build/test:'+cp,'org.junit.platform.console.ConsoleLauncher','execute','--disable-banner','--disable-ansi-colors','--class-path','build/main:build/test','--select-class','lesson.contexts.ContextsTests','--reports-dir','build/test-results','--details','tree'],'junit')
app=run(['java','-cp','build/main:'+cp,'lesson.contexts.ContextsDemo'],'application')
version=subprocess.run(['java','-version'],capture_output=True,text=True,check=True);(E/'java-version.txt').write_text(version.stderr)
reports=[]
for path in sorted((ROOT/'build/test-results').glob('TEST-*.xml')):
 tree=ET.parse(path);report=tree.getroot();reports.append({'file':str(path.relative_to(ROOT)),**report.attrib});(E/('java-'+path.name)).write_bytes(path.read_bytes())
assert any(int(float(x.get('tests','0')))==4 and int(float(x.get('failures','0')))==0 and int(float(x.get('errors','0')))==0 for x in reports)
proofs=['independent context isolation: passed','child parent fallback same instance: passed','parent cannot see child local bean: passed','local named bean shadows parent: passed']
assert all(x in test.stdout for x in proofs)
assert all(x in app.stdout for x in ['A alpha: alpha','B beta: beta','A beta: missing','A beta exception: NoSuchBeanDefinitionException','B alpha: missing','B alpha exception: NoSuchBeanDefinitionException','child shared: shared','child shared same: true','child owns shared: false','child local: local','parent local: missing','parent local exception: NoSuchBeanDefinitionException','parent active after child close: true'])
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'src').rglob('*.java'))}
(E/'java-source-hashes.sha256').write_text(''.join(v+'  '+k+'\n' for k,v in hashes.items()))
result={'spring_framework_version':'6.2.11','micrometer_version':'1.15.4','compiler':'ECJ3.40.0','class_file_target':'Java17','runtime':version.stderr.strip(),'compile_main_exit_code':main.returncode,'compile_tests_exit_code':tests.returncode,'junit_exit_code':test.returncode,'application_exit_code':app.returncode,'compile_stderr_empty':not main.stderr and not tests.stderr,'junit_stderr_empty':not test.stderr,'application_stderr_empty':not app.stderr,'junit_reports':reports,'tests_found':4,'tests_succeeded':4,'tests_failed':0,'proof_lines':[x for x in test.stdout.splitlines() if x in proofs],'application_stdout_lines':app.stdout.splitlines(),'source_sha256':hashes,'scope':'Actual Spring6.2.11 independent context registries, named-lookup parent fallback, same parent singleton reference, local-definition/enumeration boundaries, no reverse visibility, local name shadowing and child-first close.'}
result['verified_semantics']={
 'independent_registries_both_direction_isolation':'independent context isolation: passed' in test.stdout,
 'child_named_lookup_falls_back_to_parent':'child parent fallback same instance: passed' in test.stdout,
 'parent_instance_not_copied_to_child_registry':'child parent fallback same instance: passed' in test.stdout,
 'parent_cannot_see_child_local_by_default':'parent cannot see child local bean: passed' in test.stdout,
 'child_local_named_bean_shadows_parent':'local named bean shadows parent: passed' in test.stdout,
}
(E/'java-verification-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(test.stdout);print('ACTUAL APPLICATION OUTPUT\n'+app.stdout);print('Actual multiple-context tests: 4 tests passed; application exited0.')
