import os

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky
import asyncio
import nest_asyncio
import pypresence as pp
import requests
import time

nest_asyncio.apply()


class Plugin:

    DEFAULT_CLIENT_ID = "1055680235682672682"
    RPC = pp.Presence(DEFAULT_CLIENT_ID)

    # A normal method. It can be called from the TypeScript side using @decky/api.
    async def add(self, left: int, right: int) -> int:
        return left + right

    async def long_running(self):
        await asyncio.sleep(15)
        # Passing through a bunch of random data, just as an example
        await decky.emit("timer_event", "Hello from the backend!", True, 2)


    async def fetch_discord_ids(self):
        tries = 5
        while tries > 0:
            try:
                r = requests.get("https://discordapp.com/api/v8/applications/detectable")
                decky.logger.info("Fetched Discord game IDs!")
                return "Fetched Discord game IDs!"
                # return r.json()
            except Exception as e:
                decky.logger.error("Could not fetch Discord game IDs")
                await asyncio.sleep(2)
                tries -= 1
        return "Could not fetch IDs"

    async def connect_to_discord(self):
        self.RPC = pp.Presence("359509387670192128") # Stardew game ID for testing
        tries = 5
        while tries > 0:
            try:
                self.RPC.connect() # 2. Start the handshake loop
                return "Connected to Discord!"
                # return RPC 
            except Exception as e:
                decky.logger.error("Could not find Discord app. Retrying...")
                return "Error: " + str(e)
                # await asyncio.sleep(2)
                # tries -= 1

        return "Discord not detected!"

    async def update_presence(self):
        try:
            self.RPC.update(state = "not actually just testing code", start=time.time()//1) # 3. Updates our presence
            return "Status set!"
        except Exception as e:
            return "Error: " + str(e)
    

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        self.loop = asyncio.get_event_loop()
        decky.logger.info("Hello World!")

    # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
    # completely removed
    async def _unload(self):
        decky.logger.info("Goodnight World!")
        pass

    # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
    # plugin that may remain on the system
    async def _uninstall(self):
        decky.logger.info("Goodbye World!")
        pass

    async def start_timer(self):
        self.loop.create_task(self.long_running())

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky.logger.info("Migrating")
        # Here's a migration example for logs:
        # - `~/.config/decky-template/template.log` will be migrated to `decky.decky_LOG_DIR/template.log`
        decky.migrate_logs(os.path.join(decky.DECKY_USER_HOME,
                                               ".config", "decky-template", "template.log"))
        # Here's a migration example for settings:
        # - `~/homebrew/settings/template.json` is migrated to `decky.decky_SETTINGS_DIR/template.json`
        # - `~/.config/decky-template/` all files and directories under this root are migrated to `decky.decky_SETTINGS_DIR/`
        decky.migrate_settings(
            os.path.join(decky.DECKY_HOME, "settings", "template.json"),
            os.path.join(decky.DECKY_USER_HOME, ".config", "decky-template"))
        # Here's a migration example for runtime data:
        # - `~/homebrew/template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
        # - `~/.local/share/decky-template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
        decky.migrate_runtime(
            os.path.join(decky.DECKY_HOME, "template"),
            os.path.join(decky.DECKY_USER_HOME, ".local", "share", "decky-template"))
