# Bolt's Journal

## 2024-10-24 - [Init]
**Learning:** Initialized Bolt's journal.
**Action:** Use this to track critical performance learnings.

## 2024-10-24 - [Rebranding and Performance]
**Learning:** Renaming a Python package requires careful updating of all imports and entry points (Procfile, Dockerfile). `asyncio.run` inside a function called by `asyncio.to_thread` (which runs in a separate thread) can be tricky or unnecessary if the operation can be done in the main loop before offloading.
**Action:** When converting blocking code to async, perform async I/O in the main event loop whenever possible before passing data to synchronous worker threads.

## 2024-10-24 - [Memory Optimization]
**Learning:** Reading large files (2GB+) into memory (`await f.read(FULL_SIZE)`) crashes bots on low-RAM VPS.
**Action:** Always stream file operations in chunks (e.g., 10MB) using `aiofiles` or standard file I/O within a thread.
