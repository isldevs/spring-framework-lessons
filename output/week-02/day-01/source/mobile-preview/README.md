# Prepared mobile preview — unpublished

The latest brief requires manual publication approval. No Site has been registered or deployed for this lesson. The prepared page uses native video controls, inline playback and same-origin MP4/cover/SRT download links; no transcoding.

Build a local review copy after the final MP4 is verified:

```sh
python source/mobile-preview/build.py qa/mobile-player
```

Open qa/mobile-player/dist/index.html in a compatible local browser. This prepares files only; it does not start a server or publish a page. Browser and physical-phone playback must be reported only if actually tested. A phone-accessible hosted URL requires explicit owner approval first. After approval, use the exact registered Site ID via --project-id and preserve owner-private access.

Do not store deployment credentials in source. No YouTube/Facebook upload or publication is performed by this builder.
