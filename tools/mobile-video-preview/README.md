# Phone preview and download

Owner-private preview: https://isldevs-bean-naming-player.sivlayyi-bs.chatgpt.site

The user needs to preview and play the video before downloading it on a phone. Workspace links did not work for them; raw GitHub links were served as `application/octet-stream` and did not supply a player page. This page uses native `<video controls playsinline>` with a same-origin MP4 source and a separate same-origin `download` link. It does not autoplay or change the video.

The hosted source is a separate Sites repository. Site identity: `appgprj_6b047779cd208191a67df679c22738a2`. Preserve owner-private access. This is a file-delivery page, not a YouTube/Facebook publication.

Rebuild using Python 3, without dependencies:

```sh
python tools/mobile-video-preview/build.py /workspace/sites/isldevs-bean-naming-player
```

The build verifies the current Bean naming master SHA-256 and copies the HTML, MP4 and cover into `dist/`, with a static `.openai/hosting.json`. Use the Sites workflow to synchronize source and deploy the archive. Never store authentication credentials in this repository.

Checks performed: HTML controls/inline playback/source/download wiring, no autoplay, poster presence, JavaScript syntax, archive structure and unchanged MP4 hash. Native Sites deployment status is recorded in the final handoff. Browser and physical-phone playback were not tested because the required browser tool was unavailable. The narration's earlier auditory acceptance limitation remains unchanged.
