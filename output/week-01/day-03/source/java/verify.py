#!/usr/bin/env python3
"""Actual ECJ compilation, JUnit unit/Boot integration tests and Boot app execution."""
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
# Full Spring Boot startup occurs inside the first actual JUnit test.
test=run(['java','-cp','build/main:build/test:'+cp,'org.junit.platform.console.ConsoleLauncher','execute','--disable-banner','--disable-ansi-colors','--class-path','build/main:build/test','--select-class','lesson.orders.ConstructorInjectionTests','--reports-dir','build/test-results','--details','tree'],'junit')
app=run(['java','-cp','build/main:'+cp,'lesson.orders.CheckoutApplication'],'application')
version=subprocess.run(['java','-version'],capture_output=True,text=True,check=True);(E/'java-version.txt').write_text(version.stderr)
reports=[]
for path in sorted((ROOT/'build/test-results').glob('TEST-*.xml')):
 tree=ET.parse(path);report=tree.getroot();reports.append({'file':str(path.relative_to(ROOT)),**report.attrib});(E/('java-'+path.name)).write_bytes(path.read_bytes())
assert any(int(float(x.get('tests','0')))==2 and int(float(x.get('failures','0')))==0 and int(float(x.get('errors','0')))==0 for x in reports)
assert 'same gateway bean: true' in test.stdout and 'fake gateway test: passed' in test.stdout and 'receipt: APPROVED order-1042 USD 19.99' in app.stdout
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'src').rglob('*.java'))}
(E/'java-source-hashes.sha256').write_text(''.join(v+'  '+k+'\n' for k,v in hashes.items()))
result={'spring_boot_version':'3.5.6','spring_framework_version':'6.2.11','micrometer_version':'1.15.4','compiler':'ECJ3.40.0','class_file_target':'Java17','runtime':version.stderr.strip(),'compile_main_exit_code':main.returncode,'compile_tests_exit_code':tests.returncode,'junit_exit_code':test.returncode,'application_exit_code':app.returncode,'compile_stderr_empty':not main.stderr and not tests.stderr,'junit_stderr_empty':not test.stderr,'application_stderr_empty':not app.stderr,'junit_reports':reports,'tests_found':2,'tests_succeeded':2,'tests_failed':0,'proof_lines':[x for x in test.stdout.splitlines() if x in ['App starts Spring Boot','DemoGateway created','OrderService constructed with PaymentGateway','Boot context ready','same gateway bean: true','receipt: APPROVED order-1042 USD 19.99','Spring Boot integration test: passed','fake gateway test: passed']],'application_stdout_lines':app.stdout.splitlines(),'source_sha256':hashes,'scope':'Actual non-web SpringApplication startup and separate pure Java fake-gateway test; no real payment or external gateway contact.'}
(E/'java-verification-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(test.stdout);print('ACTUAL APPLICATION OUTPUT\n'+app.stdout);print('Actual Boot integration + fake gateway tests: 2 tests passed; application exited0.')
