@echo off
echo === Min Research Group Website Build ===
echo.

echo [1/3] Syncing from Notion...
python sync_notion.py
if errorlevel 1 (
    echo ERROR: Notion sync failed. Check your .env file and API key.
    pause
    exit /b 1
)

echo.
echo [2/3] Building Hugo site...
hugo
if errorlevel 1 (
    echo ERROR: Hugo build failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Done! Site built in /public
echo.
echo To preview: hugo server
echo To deploy:  git add . ^&^& git commit -m "update site" ^&^& git push
pause
