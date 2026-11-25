# Mobile preview and download

Buildless owner-private player with native video controls, inline playback and same-origin downloads for the MP4, cover and SRT. It copies the final media without transcoding. `index.html` is a template; its duration comes from the real MP4 via FFprobe.

```sh
python source/mobile-preview/build.py /workspace/sites/isldevs-context-smoke-test-player --project-id EXACT_REGISTERED_SITE_ID
```

Run from the lesson directory after rendering and validation. Pass the exact ID from Sites registration or the existing `.openai/hosting.json`; preserve the current Site's audience. Synchronize the prepared source, then package `.openai/hosting.json` and `dist/` and deploy that exact pushed source through Sites.

Never persist authentication credentials in source or archives. The returned deployment status verifies hosting; browser or physical-phone playback requires a separate actual check. Deployment details and limitations are retained in `deployment.json` when available.
