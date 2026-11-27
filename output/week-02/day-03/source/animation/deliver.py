from pathlib import Path
import json,hashlib,shutil,subprocess,zipfile
R=Path(__file__).resolve().parents[2];P=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((R/'source/evidence/final-summary.json').read_text());assert sha(R/'video.mp4')==q['sha256']
required=['video.mp4','cover.png','first-frame.png','thumbnail-style.json','subtitles.srt','subtitle-style.json','narration.wav','narration-script.md','storyboard.md','youtube-metadata.md','facebook-metadata.md','verification-report.md','asset-rights.md','originality-review.md']
assert all((R/x).is_file() and (R/x).stat().st_size>0 for x in required)
f=json.loads((R/'source/publishing-fields.json').read_text());archives=[];copies=[]
for platform,fields in [('youtube-shorts',{'title':f['title'],'description':f['description'],'tags':f['tags'],'pinned-comment':f['pinned-comment']}),('facebook-reels',{'caption':f['facebook-caption']})]:
 out=R/'platforms'/platform;out.mkdir(parents=True,exist_ok=True)
 for name in ['video.mp4','cover.png','first-frame.png','subtitles.srt','thumbnail-style.json','subtitle-style.json','platform-policy-review.md']:shutil.copy2(R/name,out/name)
 for name,text in fields.items():(out/(name+'.txt')).write_text(text+'\n')
 (out/'upload-notes.md').write_text('Publication2026-11-25, proposed19:00Asia/Phnom_Penh. Manual approval and voice listening acceptance required. Select opening thumbnail frame where supported. Review current AI controls. No publishing performed.\n')
 for label,cmd in [('probe',['ffprobe','-v','error','-show_streams','-of','json',str(out/'video.mp4')]),('decode',['ffmpeg','-v','error','-i',str(out/'video.mp4'),'-f','null','-'])]:
  p=subprocess.run(cmd,capture_output=True);assert p.returncode==0;assert not p.stderr
  (out/(label+'.txt')).write_bytes(p.stdout)
 assert sha(out/'video.mp4')==q['sha256'];copies.append({'platform':platform,'probe_pass':True,'full_decode_pass':True,'master_hash_equal':True})
 files=sorted(x for x in out.iterdir() if x.is_file());(out/'checksums.sha256').write_text(''.join(sha(x)+'  '+x.name+'\n' for x in files))
 zpath=P/(R.name+'-'+platform+'-upload.zip')
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
  for x in out.iterdir():z.write(x,platform+'/'+x.name)
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  for x in out.iterdir():assert hashlib.sha256(z.read(platform+'/'+x.name)).hexdigest()==sha(x)
 archives.append(zpath)
(R/'source/evidence/platform-copy-checks.json').write_text(json.dumps(copies,indent=2))
# No binary models, environments, caches or symlinks enter delivery.
def files():return sorted(p for p in R.rglob('*') if p.is_file() and not p.is_symlink() and not {'.venv','models','__pycache__'}.intersection(p.relative_to(R).parts) and p.suffix not in ['.pyc','.pyo'])
for p in files():
 if p.suffix=='.sh':p.chmod(0o755)
manifest=R/'checksums.sha256';manifest.write_text(''.join(sha(p)+'  '+str(p.relative_to(R))+'\n' for p in files() if p!=manifest))
count=0
for line in manifest.read_text().splitlines():
 h,name=line.split('  ',1);assert sha(R/name)==h;count+=1
zpath=P/(R.name+'-production.zip')
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files():z.write(p,R.name+'/'+str(p.relative_to(R)))
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for p in files():assert hashlib.sha256(z.read(R.name+'/'+str(p.relative_to(R)))).hexdigest()==sha(p)
archives.append(zpath);(P/(R.name+'-archives.sha256')).write_text(''.join(sha(p)+'  '+p.name+'\n' for p in archives))
(P/(R.name+'-delivery-audit.json')).write_text(json.dumps({'manifest_files_verified':count,'platform_copies':copies,'zip_crcs_and_production_member_hashes':True,'archives':[{'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in archives],'status':'INCOMPLETE for perceptual listening acceptance'},indent=2));print(count,'manifest hashes and3ZIPs verified')
