# ComfyUI YuE2 T8

[Model weights](https://huggingface.co/t8star/YuE2-Comfy) · [ComfyUI Registry](https://registry.comfy.org/nodes/yue2-t8)

![YuE2 Music T8](icon.svg)

## Full Portable Bundle

Full portable bundle: [Quark pan download](https://pan.quark.cn/s/67ebf18a2d51) · [Hugging Face download v1.5.4](https://huggingface.co/t8star/YuE2-Comfy/resolve/main/bundles/Yue2-T8-Onekey-v1.5.4-Windows-NVIDIA.rar?download=true) · [SHA-256](https://huggingface.co/t8star/YuE2-Comfy/resolve/main/bundles/Yue2-T8-Onekey-v1.5.4-Windows-NVIDIA.rar.sha256?download=true)

A complete Windows / NVIDIA package including the runtime environment and models. After fully extracting, double-click `YuE2-T8.exe` to start; on first launch you can use the "Check for updates" button on the page to install the latest small code patches.

Extract to a short directory (e.g. `E:\YuE2`). v1.5.9 shortened the checkpoint temporary paths and fixed an issue where legacy nested cover jobs could exceed the Windows 260-character limit even when the final file path was valid; if the installation directory itself is very deep, third-party components' final files may still hit system path limits.

If Windows blocks the EXE, double-click `启动本地整合包.bat` (Start Local Bundle) instead. After downloading, you can verify the full package in PowerShell:

```powershell
Get-FileHash .\Yue2-T8-Onekey-v1.5.4-Windows-NVIDIA.rar -Algorithm SHA256
```

The correct SHA-256 is `dec9319a2bed3a810e4f810524537e94920142d13d0c9b688353ddfa0e372d9b`.

[GitHub Releases](https://github.com/T8mars/Comfyui-YuE2-T8/releases) only provide code and auto-update attachments, without Python or models. Get the full portable bundle from the Quark link above; models and optional GGUF weights can also be downloaded separately from the drive links below. When a legacy-version upgrade involves unified-runtime migration, the updater downloads the needed dependencies on demand.

## Model Downloads

Model drive: [Quark pan download](https://pan.quark.cn/s/6c40eac8af6c)

See "Model placement paths" below for where to put the models.

## Local LLM Models (optional)

Local LLM models: [Quark pan download](https://pan.quark.cn/s/55eab3bb2d9b).

Used by the standalone WebUI's "AI Creation Assistant" to generate lyrics, styles and optional ABC. The API mode requires no download. For local mode, extract the models, set the GGUF directory in the assistant settings (e.g. `E:\LLM`), save, then select the model and test the connection; leaving it empty uses the `LLM` folder under the model root. This download is independent of the music model package and is not required to run YuE2.

## Overview

YuE2 Music T8 integrates YuE2-3B full-song generation into ComfyUI and ships a standalone local WebUI. The nodes call an isolated inference worker at `127.0.0.1:8189` and never replace or pollute ComfyUI's own Torch environment. 1.1.0 added Seed-VC + Demucs zero-shot reference-voice covers; 1.1.1 added a Windows EXE launcher; 1.1.2 can safely switch ports when another idle YuE2 instance occupies 8189; 1.1.3 fixed a missing YuE2 inference source in the standalone bundle and added in-page logs; 1.1.4 added configurable model directories and model-less GitHub Release update manifests.

Main features:

- Generate 48 kHz stereo songs from Chinese or English lyrics; supports the `full`, `melody` and `off` planning modes.
- Generate and save ABC melody/chord plans; restore the original plan exactly, or edit/import ABC and regenerate.
- Generate 1–8 consecutive-seed candidates per run; full song artifacts keep the request, config, tokens, latents and integrity manifest, and finished results are retained if a later candidate fails.
- Convert WAV, FLAC, MP3, M4A, OGG and AAC to ABC/MIDI with SheetSage2 + MERT and generate covers.
- Feed a 1–30 second reference vocal to convert the generated song's vocals to the reference timbre, then remix with the Demucs-separated accompaniment into 48 kHz stereo FLAC.
- The Seed-VC and RVC cover sections offer one-octave-down, original-pitch and one-octave-up shortcuts directly: female original with male voice usually starts at −12, male original with female voice usually starts at +12; you can also enter any integer semitone from −12 to +12.
- Shared single-GPU queue, job center, per-job cancellation, job history and export; the job center distinguishes the current job and shows the real waiting total, plus the source, stage, style summary and actual queue order of the last 100 jobs.
- Automatic cleanup of expired or over-quota jobs, uploads and logs; important results in `exports` are kept forever, and interrupted jobs are explicitly marked failed on service restart.
- MuLaCover remixing can extract melody, chords and drums from a full song automatically or read MIDI directly; supports new lyrics, structured styles, transposition, fixed seeds, auditioning and MIDI export, and can send the result on to Seed-VC/RVC voice conversion.
### v1.5.12: ten-round cross-checks, cleanup retries, and generation-condition fixes

- Generation, test and retry operations lock immediately while the assistant is submitting a job, so double-clicks cannot create duplicate paid jobs; project switching waits for submission, and draft-save failures still track the created job.
- Deletion strictly limited to preview-allowed assets was removed entirely; more than 500 protected materials no longer block cleanup of eligible ones. Retries continue when files or waveform caches are locked; partial Windows cleanup keeps the job record and a clear explanation.
- Stale responses are discarded when switching projects or refreshing model lists; training "add songs" opens the normal asset library, and pagination realigns after screen-size changes. The style model selected "for song creation" is saved to the project draft as well.
- The instrumental-only checkbox now actually converts to a model text condition without vocals plus an `[instrumental]` lyrics marker, ignores original lyrics and removes common affirmative vocal hints. The model may still produce vocal-like sounds; the option cannot hard-guarantee no vocals (Issue #12).
- Remixing gained a default "no style specified" mode where theme, genre, instruments and mood can be left empty, switchable to a specified style. The reference provides melody, chords and drums; this mode cannot guarantee a full copy of the original arrangement or timbre (Issue #13).

### v1.5.13: training runs, checkpoints, and snapshot cleanup

The "Training workbench" gained "Clean up training runs & snapshots - Manage / Clean up", listing runs and snapshots 10 per page with cross-page selection. Before confirming, it shows the deletion scope, preprocessing caches and checkpoint space, and the retention reasons for shared snapshots, running jobs and drafts. Pausing a run requires explicitly giving up continued training; locked files leave a retryable record so training cannot resume from a broken cache. Cleanup keeps original audio, models saved in the asset library, song results and exports; after deleting snapshots with no other linked training, previously snapshot-protected materials can be cleaned too.

### v1.5.11: asset recycle bin and batch job cleanup

- The asset library supports cross-page selection, moving to recycle bin and restoring; the recycle bin offers permanent deletion of selected items and emptying, with counts, references and reclaimable space previewed first.
- Project references are kept by default; when deletion is truly needed you can explicitly also remove them from projects. Materials used by training snapshots, trained models, running jobs and drafts stay protected, and shared files are released only after the last asset is deleted.
- "Jobs & versions" supports per-item or batch cleanup, plus cleaning failed/cancelled jobs by current filter; scope and space are shown before confirmation, and running, queued, paused and still-referenced jobs are kept.
- Job cleanup preserves the asset library, models, training data and exported files; recycled assets can be restored, and only permanent deletion frees space. Retries are supported when files are locked, and deleting the last page returns to a valid page.

### Standalone bundle API

After the bundle starts, the web page and API share one address, by default `http://127.0.0.1:8189`; if the launcher sets another port, use the port shown in the browser address bar. `GET /api/health` checks service and model status, `POST /api/jobs` submits jobs, `GET /api/jobs/{job_id}` queries progress and results, and `POST /api/jobs/{job_id}/cancel` cancels a job. These local endpoints work without installing ComfyUI.

```powershell
Invoke-RestMethod http://127.0.0.1:8189/api/health
Invoke-RestMethod http://127.0.0.1:8189/api/jobs -Method Post -ContentType 'application/json' -Body '{"kind":"generate","request":{"style":"acoustic folk, piano","lyrics":"[Verse] Hello again","cot":"off","seed":831001}}'
```

Submission returns a job ID and generation runs queued in the background. See `client.py` in the repository for a Python example.


### v1.5.10: AI assistant model list refresh fix

- "Save settings / refresh models" now saves the address and credentials, then actually requests that channel's model LIST; if a compatible endpoint has no model selected, the first list item is auto-selected and saved.
- The model list survives page refreshes; manually entered models are not overwritten by refreshes. Lists and credentials are isolated per API address, so results from an old address never overwrite the current list.
- When the endpoint lacks `/models`, authentication fails or the list is empty, the specific reason is shown while keeping settings and the custom-model entry; without a model ID no paid creation or connection test starts.
- Verified saving, list reading, refresh recovery, manual models, 404 fallback and delayed responses with a real browser against a local HTTP-compatible endpoint; refreshing the list alone sends no chat request.

### v1.5.9: Windows checkpoint temporary path fix

- Stage temporary directories changed from `semantic.tmp-<full UUID>` to short random directories, and JSON temp files no longer stack the target name, PID and full UUID.
- Temp directories still live next to the final checkpoint and are committed atomically after all files are written; cancellation or failure never exposes half-written data, and old checkpoints and the resume format stay compatible.
- Added regression checks for user-reported 262-character path errors and near-limit installation directories; no registry edits are needed to resolve that error.
- Fixed Issue #9: restored MuLaCover codec and torchtune Python sources wrongly excluded by ignore rules; readiness is no longer reported when sources are missing, and release packages force-check required files.

### v1.5.8: ten-round cross audit and release-chain fixes

- Fixed duplicated pages and missing songs when the same material was added to a project with multiple roles; empty pitch input, wrong boolean types and invalid JSON now get clear error messages before queueing.
- Invalid ABC is still fully preserved and can be sent; manual validation failures never overwrite recovery instructions; assistant settings load, project switching and refresh recovery no longer overwrite each other.
- The mobile asset library shows 8 items per page with pagination at the top of the list; duplicate buttons carry the work's title, the first Tab reaches "skip to main content", and failed training-resource checks get a clear retry entry.
- After a successful Windows launch the launcher file is released immediately, so in-page auto-updates are no longer locked by the EXE; Comfy Registry publishes only from version tags that pass full CI, keeping node package and release tag contents consistent.

### v1.5.7: interaction polish and job recovery

- Project renaming, archiving, updating, cleanup and voice management now use in-workbench dialogs instead of browser-native prompt boxes that interrupt work.
- The AI assistant excludes connection tests server-side before finding the current project's latest real creation, so repeated model tests never hide lyrics, style or ABC results.
- Windows launcher, updater, Python, web pages and browser regressions are all covered by a single all-green release check.

### v1.5.6: ten-round cross-checks and large-data stability

- Fixed a concurrency race where clicking cancel right after a job finished could overwrite the finished output; completion states and submitted results are no longer rewritten by stale state.
- The job center can recover the current job beyond the last 100 records and shows the true queue total; the AI assistant recovers jobs per project, and paid actions are disabled with a clear entry point when no API key or GGUF is configured.
- Training runs, models and training materials are no longer silently truncated at 200/500 items; project song versions show 8 per page, project materials 10 per page, and trained models 3 per page.
- Added a keyboard "skip to main content" link, a clearer mobile menu and precise score descriptions; the launcher now writes real version info, verified by Windows CI.

### v1.5.5: long ABC output budget

- New installs of the AI Creation Assistant raise the default output budget from 4K to 32K; cloud APIs and compatible endpoints accept up to 262,144 tokens, covering the user-requested 220K.
- Cloud and local GGUF remember their budgets separately; switching to a local model defaults back to 4K to avoid exceeding local context. Final output capability and cost still depend on the chosen model and channel.

### v1.5.4: background progress and full-bundle delivery

- RVC material slicing, F0, HuBERT features and training epochs all report numeric progress to background jobs, visible after switching pages.
- Full-bundle builds verify and include all four MuLaCover model groups, example RVC/YuE2 models and the native ComfyUI MuLaCover node pack.

### v1.5.3: workbench and ComfyUI training pipeline

- When sending large audio from the asset library or job results, the browser only passes validated local references; the server hands them to the job via hard link or local copy, avoiding a full-song download-and-reupload through browser memory.
- "YuE2 Generate Song" can select a trained song style LoRA, set 0-2 strength, or connect the output of "YuE2 Train Song Style" directly; the style LoRA currently works only in the validated direct-generation mode.
- New RVC voice loading, training and cover nodes. Training projects, material auditioning, speakers and training parameters are prepared in the local workbench; the node runs a preflight and hands the trained voice straight to RVC cover.
### v1.5.2: training, recovery and update stability review

- YuE2 training only accepts complete songs or works of at least 5 seconds; train/validation sets use server-recorded song sources so different segments of one song cannot be mistaken for two songs.
- RVC materials must be explicitly marked as vocals-only; accompanied or unconfirmed materials are guided to separation first, preventing howling and constant noise from wrong training.
- Project drafts cover AI creation, YuE2 training and MuLaCover; each project's content is restored after page switches, and archived projects can be restored directly.
- Current results are restored per project and panel from the full job library; the job list uses lightweight state and no longer slows down as history stage arrays grow.
- Training materials can be auditioned directly, finished models show steps, time and source; MIDI and ABC job results enter the asset library automatically.
- Fixed the updater locking up permanently after an abnormal exit; the unified installer prepares RVC and MuLaCover models, while code updates still exclude Python, models or user data.
- Mobile reorders the training form and adds a four-step onboarding; desktop, tablet and phone browser regressions cover project isolation, archived recovery and training drafts.

### v1.5.0: MuLaCover native remixing

- The standalone workbench gained "Remix": reference song or MIDI, lyrics and style are all saved in the current project draft and survive page switches or refreshes.
- Jobs show real background stages "extract melody - encode style - generate - decode", with cancel, retry, in-page audition and melody/chord/drum MIDI export.
- MuLaCover, HeartCodec, Qwen3 Embedding and transcription components share one Python 3.12 runtime, loading sequentially on demand and releasing VRAM after each job.
- A separate native ComfyUI node repository is available at [Comfyui-Mulacover-T8](https://github.com/T8mars/Comfyui-Mulacover-T8) without depending on this workbench's HTTP service; both can share the same model directory.

### v1.4.9: cover vocal-range quick controls

- Seed-VC's singing pitch moved from advanced settings into the main cover flow, showing one-octave-down, original and one-octave-up shortcuts just like RVC.
- "Female song, male voice - octave down" corresponds to -12 semitones and "male song, female voice - octave up" to +12; the choice is remembered per browser.
- Octave shifts only change the pitch of the separated vocals; the accompaniment is untouched. Non-whole octaves can clash with the original accompaniment, and the page warns about this explicitly.

### v1.4.8: UI contrast and full review

- Deepened the colors of section numbers, primary action buttons, flow completion states and history completion states; small text meets WCAG AA contrast.
- Running or queued jobs show a persistent background progress card with the backend-reported percentage, counts or current stage; clicking returns to the full job details.
- Re-covered first launch, project creation, all 9 workspaces, keyboard dialogs, refresh states after adding assets to a project, and desktop, tablet and phone layouts.
- GitHub auto-update packages still contain code only - no Python, models, GGUF, local assets or user data.

### v1.4.7: player and error-message accessibility

- Current results, history, multi-candidate, stems, RVC, training short auditions and the global player all have clear, distinguishable screen-reader names.
- Text asset viewers got names, and workspace buttons use correct current-page semantics.
- Multi-candidate jobs with partial success no longer show raw technical exceptions; full details remain in the job log.
- Browser regressions directly check audio players, dynamic dialog controls, navigation semantics and partial-result error summaries.

### v1.4.6: asset-added-to-project state fix

- When an asset's current version is already in the selected project, the button reliably shows "Already in project" instead of appearing unresponsive after repeat clicks.
- After an asset gains a new version it can be added to the project again, and the project stays pinned to the specific version the user explicitly added.
- Browser regressions cover both added and not-yet-added asset cards; GitHub auto-update packages still contain code only.

### v1.4.5: asset actions, page switching and failure messages

- Asset card audition, send, edit and add-to-project actions wrap properly; common desktop widths no longer get horizontal scrolling or clipped buttons.
- Phones and tablets return to the top of a new page when switching workspaces on long pages; unrelated pages no longer briefly retain the previous page's result cards.
- Asset dialogs got screen-reader names, required fields show consistent messages; the current creation page and history page use the same friendly error summaries, with full technical details in the job log.
- Browser regressions now load a fixed project, four materials and one finished audio, and actually check asset card boundaries, three dynamic dialogs, cross-page scrolling and the current-page player.
- Legacy "update finished" records no longer conflict with current version state. GitHub auto-update packages still contain code only.

### v1.4.4: mobile all-features menu and browser regressions

- Phones and tablets gained an always-visible "All" entry at the top that opens all 9 workspaces and marks the current page; no more relying on users discovering horizontal swiping.
- GitHub Quality gained a real Chromium regression checking navigation, project focus, empty-filter recovery, button states, control names, duplicate IDs, page overflow and console errors across desktop, tablet and phone.
- Every quality check saves desktop, tablet, phone and phone-menu screenshots plus browser and service reports, making future style regressions easier to spot.
- Update sync excludes `.git`, virtual environments, test caches and `node_modules`, and retries transient Windows file locks; official auto-update packages still contain versioned code only.

### v1.4.3: workbench navigation and onboarding fixes

- Desktop keeps only the left workbench navigation; phones and tablets compress the header and self-check area so the current feature enters the first screen sooner.
- At 1024 px and below the current project stays visible with one-click return to project selection, reducing the risk of putting results into the wrong project.
- Storage cleanup explains its scope and asks for confirmation first; the cancel button is disabled when nothing is executing; history technical errors show a friendly summary first, with details and logs still expandable.
- Asset and job filters offer one-click clearing when empty, and search, score editing and upload controls got proper accessible names and text contrast.

### v1.4.2: project races and narrow-window fixes

- Upload, generate, transcribe, cover, training and assistant jobs always belong to the project active when they started; switching projects mid-operation no longer crosses results, drafts or errors into the new project.
- YuE2 training, checkpoint auditioning and assistant jobs are displayed separately; auditioning never overwrites the safe pause/resume state, and sending to creation uses the checkpoint model the user explicitly picked.
- ABC scores in the asset library can be sent straight to the editable score plan, with audition results staying in the original project; slow project, asset and history requests never overwrite newer selections.
- At 1024 px and below the top workspace navigation becomes horizontally scrollable and auto-scrolls the current feature into view; model settings collapse after page switches, so forms and results are no longer squeezed by the sidebar.
- Release packages still contain only code and the auto-update manifest - no Python, music models, GGUF, local works, user data or private roadmap.

### v1.4.1: workbench end-to-end and training data fixes

- Projects, assets, creation and training are now truly connected: assets can be sent directly to original-song, reference-voice, RVC, lyrics, style and score inputs; text is editable, and both assets and jobs support filtered pagination.
- Project drafts are isolated per project; switching, archiving, refreshing and load failures never leak into other projects. Projects can be renamed, archived, have materials removed, select a main version, and export audio with checksums to `exports`.
- YuE2 training binds lyrics, style or an explicit instrumental marker per song; the backend forbids the same audio in both train and validation sets. After pausing, any complete checkpoint can be auditioned, with training identity, steps and all file hashes verified first.
- Model settings are reachable from every page; mobile keeps a single workbench navigation with better touch sizes. History jobs support status, type, project and text filters.
- GitHub Releases still contain only code auto-update packages - no Python, models, GGUF or user data; the Windows / NVIDIA full bundle keeps coming from the Quark link at the top of the page.

### v1.4.0: music workbench, asset library and YuE2 style training

- The standalone WebUI became a unified music workbench: projects, asset library, creation, scores, reference voice, AI assistant, training and history share one navigation and current project.
- The asset library manages songs, works, vocals, accompaniments, reference voices, lyrics, styles, scores and models uniformly. Imported audio can be played, waveform-viewed and pinned as a version into a project immediately; job results are archived automatically.
- The "Training workbench" builds immutable train/validation snapshots from at least two different songs, requires confirming material rights, trains a YuE2 AR LoRA on MERT features, and shows progress, train/validation loss, pause and resume.
- Style models are automatically paired with the pinned Mothersuperior v4 NAR companion resources. After training, an about-10-second audition is generated on the same page and can be sent to song creation; the first phase only opens the machine-validated "direct generation" mode.
- RVC continues to serve dedicated singing-voice training and YuE2 LoRA serves song style, with a clear division inside the workbench. All features keep sharing one `runtime/python.exe`.

### v1.3.1: VRAM control, recovery and release gates

- ComfyUI and the standalone WebUI use the same editable VRAM budget, no longer limiting node inputs to 12-24 GiB.
- Failed-job recovery adopts the page's current VRAM budget; VAE tiling respects both physical VRAM and the user budget.
- ROCm/HIP uses compatible decode and Seed-VC paths and disables experimental FP8 that produced wrong results; an official ROCm full runtime still needs acceptance on real AMD hardware.
- Auto-updates clearly state where code backups go before starting; GitHub PRs run the full test suite, and release jobs fail visibly when the Registry has not accepted the version.

### v1.3.0: unified runtime and RVC training workbench

- All local features share Python 3.12.10 / Torch 2.10.0 + CUDA 12.8, running stage-by-stage subprocesses.
- "My voices / Training": import materials, audition and filter, separate accompaniment, train, cancel/resume, build index, voice library preview and import/export. Users without RVC models can train right on the page.
- The cover page converts existing songs directly, or remixes with YuE2 first; choose Seed-VC, RVC or a same-song comparison. Comparisons share stem caches, and both the current page and history keep playable results.
- RVC shows training vocal-range statistics for the selected voice, with separate semitone and octave controls and an option to disable index retrieval. Original pitch is the default; octave-down changes singing pitch and does not affect Seed-VC pitch in comparison mode.
- Training projects/caches, materials and the user voice library can be moved to custom directories with validated migration; original data is kept as a backup. The updater supports legacy multi-runtime migration and rollback on failure.

RVC training and conversion have been verified in practice; a few samples cannot prove every voice works, and no promise is made that RVC always beats Seed-VC. Public material comparison metrics and human blind-listening status are in the release attachment [RVC_EVALUATION.md](https://github.com/T8mars/Comfyui-YuE2-T8/releases/download/v1.3.0/RVC_EVALUATION.md). The full bundle ships a compiled, verified optional FlashAttention wheel; current song inference does not use a separate `flash_attn`, nothing needs installing, and no full-song speedup is claimed.

### AI Creation Assistant (standalone WebUI)

The "AI Creation Assistant" generates lyrics, styles and optional ABC through Zhenzhen's budget house, Zhenzhen's AI workshop, an OpenAI-compatible endpoint or local GGUF. Results can be edited, saved and downloaded, then sent field-by-field to "Creation", "Score plan" or "Melody cover / Reference voice". Sending only fills the draft; audio generation is started by buttons on the target page; the feature adds no ComfyUI nodes.

## Installation

After the Registry version is reviewed, install via ComfyUI Registry/Manager:

```bash
comfy node install yue2-t8
```

Or install manually:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/T8mars/Comfyui-YuE2-T8.git
```

After installing the nodes, enter the node directory and run `install_runtime.bat` once. The script downloads the models, the unified Python 3.12.10 runtime with the RVC base models, CUDA 12.8 Torch, FFmpeg and the offline score-rendering components. Restart ComfyUI afterwards.

Requirements: Windows 10/11, an NVIDIA GPU, 24 GB VRAM recommended, and at least 60 GB free disk space for installation, downloads and migration (training materials, checkpoints and works extra). Normal generation, transcription and reference-voice conversion all run offline.

## Model placement paths

Models are published uniformly at [t8star/YuE2-Comfy](https://huggingface.co/t8star/YuE2-Comfy). The install script pins the verified model commit [`a083f1064`](https://huggingface.co/t8star/YuE2-Comfy/commit/a083f106499daead99259dd0c443a5494254cfc5). By default they go into the node directory's `models`; you can also expand "Model location & install notes" at the top of the WebUI to set an absolute path on another drive, or double-click `configure_models.bat` before installing. The current path is stored in `settings.json`.

```text
ComfyUI/custom_nodes/yue2-t8/models/YuE2-3B/model.safetensors
ComfyUI/custom_nodes/yue2-t8/models/YuE2-Vae/model.safetensors
ComfyUI/custom_nodes/yue2-t8/models/SheetSage2/model.safetensors
ComfyUI/custom_nodes/yue2-t8/models/MERT-v2-FullSong/model.safetensors
ComfyUI/custom_nodes/yue2-t8/models/SheetSage2/render_assets/
ComfyUI/custom_nodes/yue2-t8/models/Seed-VC/DiT_seed_v2_uvit_whisper_base_f0_44k_bigvgan_pruned_ft_ema_v2.pth
ComfyUI/custom_nodes/yue2-t8/models/Demucs/955717e8.safetensors
ComfyUI/custom_nodes/yue2-t8/models/RVC/
ComfyUI/custom_nodes/yue2-t8/models/YuE2-training/
ComfyUI/custom_nodes/yue2-t8/models/MuLaCover/
ComfyUI/custom_nodes/yue2-t8/models/HeartCodec-oss/
ComfyUI/custom_nodes/yue2-t8/models/Qwen3-Embedding-0.6B/
ComfyUI/custom_nodes/yue2-t8/models/SymbolicTranscriptor/
ComfyUI/custom_nodes/yue2-t8/models/VOICE_MODEL_MANIFEST.json
```

When cloning with git manually, replace `yue2-t8` above with the actual repository directory name `Comfyui-YuE2-T8`. Do not put weights directly into ComfyUI's `checkpoints` directory; the code needs the twelve model subdirectories with their configs and manifests kept intact. `YuE2-training` is about 414 MB; the four MuLaCover directories can be fetched with `scripts/download_mulacover_models.py --root <bundle directory>` and verified against pinned versions. The native [Comfyui-Mulacover-T8](https://github.com/T8mars/Comfyui-Mulacover-T8) model loader can also take this `models` absolute path directly, avoiding duplicated large-model storage.
## Community training examples

[CSD Korean Female v1](https://huggingface.co/t8star/YuE2-Comfy/tree/main/Community-Models/CSD-Korean-Female-v1) provides an importable RVC singing-voice package, a YuE2 AR style LoRA, a pinned NAR companion and three auditions. The RVC voice was trained for 100 epochs on 46 recordings totaling 68.5 minutes; the YuE2 LoRA ran 800 steps and selected the step-200 checkpoint with the lowest validation loss on a song-disjoint validation set. New complete bundles ship with both trained examples preinstalled.

The material comes from one unnamed professional Korean female singer documented in CSD v1.1, not Go Youn-jung. CSD derivatives and auditions are CC BY-NC-SA 4.0, non-commercial use only; the pinned NAR companion keeps Mothersuperior's CC BY-NC 4.0, and the RVC package also retains its upstream agreement. Defer to the per-file manifests, credits and license files inside the model directory.

## Updating

Since v1.2.2, the runtime status card at the top right of the local WebUI home offers a "Check for updates" button, and stable releases are checked automatically when the page opens. When a new version is found, click "Update to vX": the program downloads the code package from the [latest release manifest](https://github.com/T8mars/Comfyui-YuE2-T8/releases/latest/download/update-manifest.json), verifies origin and SHA256, backs up the old code, installs and restarts on the current port. Updates keep models, local GGUF, works, uploads, exports, logs, caches, assistant drafts and settings. The first upgrade to v1.3.0 prepares and validates the unified runtime, completes RVC base models, and switches code and Python only after the old service exits; the new service cleans old runtimes only after passing startup checks, and restores old code and the original runtime on failure. Updates do not start while jobs are running or queued.

GitHub `*-code.zip` files are code packages for auto-update, without models or Python; the full bundle includes the unified runtime and base models, with GGUF weights chosen separately. The in-page updater is available since v1.2.2. For earlier versions, extract the new full bundle into a new directory, point it at the existing model path, and keep the old installation and works.

Do not just overwrite v1.3.0 code onto an old multi-Python bundle: the new version needs unified-runtime migration. Use the in-page updater, or install the full bundle in a new directory. The first upgrade needs network access for missing components and temporary space for old and new environments side by side; already-validated models are reused.

1.1.5 fixed the VRAM peak of long-song acoustic synthesis on Windows, chunking queries and offloading idle AR weights by default; reference-voice covers became persistent background jobs with staged saving and resumption. When finished, the current page shows a player, duration and download button directly, and recent works survive refreshes and page switches. See [VALIDATION.md](VALIDATION.md).

## Usage

The nodes live in the `YuE2 Music` category. The `workflows` directory provides six workflow types: lyrics-to-song, plan-then-render, external ABC regeneration, reference-voice cover, YuE2 song style training, and RVC training & cover. On the Windows bundle, double-click `YuE2-T8.exe` to start; for the node source package, double-click `start_webui.bat`. The launcher window stays open showing the service address or the failure reason. If 8189 is already used by another idle YuE2, the launcher verifies the process and switches automatically; it never interrupts running or queued jobs. `stop_service.bat` stops the background service manually.

Reference-voice covers need a clear 1-30 second single-vocal dry recording, ideally 5-25 seconds, unaccompanied, with little reverb. The workflow first generates or receives the song, then separates vocals/accompaniment, converts the timbre and remixes. Only use your own voice or voices you have explicit permission to use.

On first use, run the "YuE2 Model Service" node or the WebUI self-check in the top right. All output is saved under `outputs/jobs` in the node directory, and exported results in `exports`. Failed jobs can be expanded with logs directly on the WebUI "Jobs & versions" page, or under the node directory's `logs`; the page shows the worker's concrete exception instead of just an exit code.

The retention policy is written to `retention.json` in the node directory on first launch: finished jobs are kept 30 days, at most 100 jobs and 100 GiB total; uploads 7 days and at most 10 GiB; regular logs 30 days and at most 2 GiB. The service runs it every 6 hours, and it can also be triggered manually on the "Jobs & versions" page. Export results you want to keep into `exports`; the automatic policy never deletes that directory.


With a custom directory, that directory itself is the `models` in the paths above: the twelve subdirectories and the manifests must sit directly inside it. Command-line installation also supports:

```powershell
## Nodes

| Node | Function |
| --- | --- |
| YuE2 Model Service | Check runtime, models and the shared service |
| YuE2 Generate Song | Lyrics, style, ABC to full audio |
| YuE2 Plan Song Score | Generate only an editable ABC plan |
| YuE2 Render Plan Score | Restore exactly or regenerate after edits |
| YuE2 Audio Transcribe | Audio to ABC, MIDI, events and rendered score |
| YuE2 Melody Cover | Generate with a reviewed ABC and a new style |
| YuE2 Reference Voice Cover | Convert vocal timbre with Seed-VC + Demucs and remix |
| YuE2 Load RVC Voice | Pick a trained or imported RVC voice and speaker from the local voice library |
| YuE2 RVC Cover | Separate a full song, convert vocals with RVC and remix with the original accompaniment |
| YuE2 Train RVC Voice | Train a preflight-checked RVC project from the workbench and return the voice |
| YuE2 Train Song Style | Preprocess and train the workbench's YuE2 AR LoRA; connect the result directly to generation |
| YuE2 Generate Semantic Tokens | Advanced staged inference |
| YuE2 Acoustic Synthesis | Semantic tokens to acoustic latents |
| YuE2 VAE Decode | Latents to 48 kHz stereo audio |
| YuE2 Export Artifacts | Copy full artifacts to `exports` |
| YuE2 Unload/Cancel | Query or cancel the current isolated worker |

## Links

- Creator: Bilibili creator T8star-Aix
- GitHub: https://github.com/T8mars/Comfyui-YuE2-T8
- Bilibili: https://space.bilibili.com/385085361
- YouTube: https://www.youtube.com/@T8star-Aix/
- API: https://api.seedance.nz/sign-up?aff=5f4w
- Online AI apps: https://www.runninghub.ai/zh-cn/user-center/1907375370302308353/userPost?inviteCode=rh-v1121
- ComfyUI portable package: https://pan.quark.cn/s/67ebf18a2d51
- Full portable bundle on Hugging Face: https://huggingface.co/t8star/YuE2-Comfy/resolve/main/bundles/Yue2-T8-Onekey-v1.5.4-Windows-NVIDIA.rar?download=true
- Hugging Face: https://huggingface.co/t8star
- Model repository: https://huggingface.co/t8star/YuE2-Comfy
- Release validation: [VALIDATION.md](VALIDATION.md)

## License

YuE2 first-party inference code and model weights are licensed under CC BY-NC 4.0 and are for non-commercial use. Seed-VC source is GPL-3.0. Demucs, BigVGAN and other third-party components retain their own licenses; see `THIRD_PARTY_NOTICES.md`, `MODEL_LICENSE`, `vendor/seed-vc/LICENSE`, and `vendor/licenses`.

This integration vendors YuE2 inference code version 0.1.6 from commit `8e06871aa2e704d87ffb9bc71b5f5420f6813724` of https://github.com/multimodal-art-projection/YuE.

.\\install_runtime.bat -ModelsDirectory "D:\\AI\\YuE2-models"
```

