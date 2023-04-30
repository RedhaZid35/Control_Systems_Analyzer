from cx_Freeze import setup, Executable

# Change these values to match your app
app_name = "MyApp"
app_version = "1.0"
app_description = "My awesome Python app"
app_executable = "./MyApp.py"

# Dependencies for your app
includes = []
packages = []
excludes = ["main.py", ]

setup(
    name=app_name,
    version=app_version,
    description=app_description,
    executables=[Executable(app_executable)],
    options={
        "build_exe": {
            "includes": includes,
            "packages": packages,
            "excludes": excludes
        }
    }
)
