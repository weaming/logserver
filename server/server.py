#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 KuraLabs S.R.L
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from pathlib import Path
from contextlib import closing
from asyncio import get_event_loop

from aionotify import Watcher, Flags
from aiofile import AIOFile, LineReader
from fastapi import FastAPI
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND
from starlette.websockets import WebSocket

app = FastAPI()


@app.websocket('/follow/{filename}')
async def handle(filename: str, response: Response, websocket: WebSocket, n: int = 1):
    # Check file exists
    cleanfn = Path(filename).name
    fnpath = Path().cwd() / cleanfn

    if not fnpath.is_file():
        response.status_code = HTTP_404_NOT_FOUND
        return

    await websocket.accept()

    # Create watcher for file
    with closing(Watcher()) as watcher:
        watcher.watch(path=str(fnpath), flags=Flags.MODIFY)
        await watcher.setup(get_event_loop())

        async with AIOFile(fnpath, mode='r', encoding='utf-8') as afd:
            reader = LineReader(afd)
            i = 0
            async for line in reader:
                i += 1
                # print(line, end='')
                if i >= n:
                    await websocket.send_text(line)

            while True:
                event = await watcher.get_event()
                print('Got event: {} {}'.format(filename, event))
                async for line in reader:
                    # print(line, end='')
                    await websocket.send_text(line)
