#!/usr/bin/env python

import sys
import asyncio
import socket

import asyncpg


async def main():
    retries_left = retry_times

    if retry_times < 1:
        retries_left = 1

    while retries_left:
        try:
            conn = await asyncpg.connect(db_dsn, timeout=int(timeout))
            break
        except asyncpg.PostgresError as err:
            retries_left -= 1
            print(f"got: {err}. retries left: {retries_left}")
        except socket.error as err:
            retries_left -= 1
            print(
                f"got: {err}",
                f"sleeping: {timeout}",
                f"retries left {retries_left}",
                sep=";",
            )
            await asyncio.sleep(timeout)

    else:
        print("exiting; db was never connected")
        sys.exit(1)

    with open(script_path, "r") as fp:
        cmds = fp.read().split(";")

    async with conn.transaction():
        for cmd in cmds:
            if cmd and (cmd := cmd.strip()):
                await conn.execute(cmd)


if __name__ == '__main__':
    db_dsn = sys.argv[1]
    script_path = sys.argv[2]

    retry_times = int(sys.argv[3])
    timeout = int(sys.argv[4])

    asyncio.run(main())
