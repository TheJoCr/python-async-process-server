from starlette.responses import JSONResponse, FileResponse, StreamingResponse
from starlette.background import BackgroundTask
import asyncio

process_id = 1

async def check_health( request ):
    output = { 'Health': 'Green' }
    return JSONResponse( output )

async def _process_as_generator( process ):
    # It would also be possible to write this data to disk as we go so that
    # other people can read it if necessary.
    sr = process.stdout
    data = await sr.read(8)
    while data != b'':
        yield data
        data = await sr.read(8)
    # Ensure the process is fully ended.
    await process.wait()
    yield f"Processes exited with code {process.returncode}"

async def run_process( request ):
    body = await request.json()
    global process_id
    process_id += 1

    # Start the process
    cmd =  'for i in 1 2 3 4 5; do sleep 1; echo "Slept $i"; done;'
    proc = await asyncio.create_subprocess_shell(
            cmd, 
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT )

    return StreamingResponse( _process_as_generator( proc ) )

async def start_process( request ):
    body = await request.json()
    global process_id
    process_id += 1
    output = { 'id': process_id }

    # Start the process
    process = await _start_process( 'for i in 1 2 3 4 5; do sleep 1; echo "Slept $i"; done;', process_id )

    # Create a BG task in charge of monitoring the process until it returns
    bg = BackgroundTask( _monitor_process, process=process )

    # And return a JSON response indicating that we've started the process
    # correctly.
    return JSONResponse( output, background=bg )
    
async def _start_process( cmd, process_id ):
    # Coroutine for actually starting a subprocess with correct stdout/stderr
    # configuration
    with open( f"log_{process_id}", 'w' ) as log_file:
        proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=log_file,
                stderr=asyncio.subprocess.STDOUT )
    return proc

async def _monitor_process( process ):
    # Coroutine that waits until the process completes
    await process.communicate()
    print( f'Process executed with return code { process.returncode }' )
    return

async def get_process( request ):
    process_id = request.path_params['id']
    with open( f"log_{process_id}", 'r') as log_file:
        return JSONResponse( { "id": process_id, "log": log_file.read() } )

async def watch_log( request ):
    process_id = request.path_params['id']
    return FileResponse( f"log_{process_id}" )

