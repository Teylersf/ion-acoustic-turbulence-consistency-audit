"""Verify bundled source-provenance copies offline; no PDFs, network or solver."""
from pathlib import Path,PurePosixPath
import hashlib,json,platform

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 if not __debug__:raise RuntimeError('Exact copy checks require assertions; -O is not supported.')
 manifest=json.loads((HERE/'integration-manifest.json').read_text(encoding='utf-8'))
 assert manifest['manifest_self_excluded']
 before={}
 for item in manifest['files']:
  name=PurePosixPath(item['package_path'])
  assert not name.is_absolute() and '..' not in name.parts
  p=(ROOT/Path(*name.parts)).resolve();assert p.is_relative_to(ROOT.resolve())
  assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],item['package_path']
  before[item['package_path']]=sha(p)
 deposit=json.loads((HERE/'public-input-deposit-verification.json').read_text(encoding='utf-8'))
 assert deposit['file_count']==len(deposit['files'])==13
 for item in deposit['files']:
  p=ROOT/'third_party/2023_JPP_iat'/item['name'];b=p.read_bytes()
  assert len(b)==item['bytes'] and sha(p)==item['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==item['Git_blob_SHA1']
 assert all(sha(ROOT/k)==v for k,v in before.items())
 result={'status':'passed','python':platform.python_version(),'program_sha256':sha(Path(__file__)),
         'manifest_sha256':sha(HERE/'integration-manifest.json'),'bundled_files_checked':len(before),
         'all_13_input_files_equal_recorded_Git_blobs':True,'all_bundled_inputs_byte_unchanged':True,
         'source_identity_semantics':'Source PDF/source-module hashes are recorded acquisition identities; absent PDFs and historical solver modules are not rehashed by this offline program.',
         'original_source_PDF_or_solver_code_required':False,'network_or_Git_required':False,
         'simulation_or_source_Lua_executed':False}
 (HERE/'integration-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({'status':'passed','bundled_files_checked':len(before),'input_files_Git_verified':13}))

if __name__=='__main__':main()
