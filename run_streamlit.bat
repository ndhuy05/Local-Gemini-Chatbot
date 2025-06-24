@echo off
echo Running Streamlit app...
python -m streamlit run %*
if errorlevel 1 (
    echo.
    echo There was an error running the Streamlit app.
    echo Make sure you have streamlit installed with: pip install streamlit
)
pause
