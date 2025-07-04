from setuptools import setup, find_packages

setup(
    name="energy_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.25.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "plotly>=5.3.0",
        "python-dateutil>=2.8.0",
        "pytz>=2021.1",
        "smolagents==1.17.0",
        "smolagents[gradio]=1.16.0",
        "arize-phoenix==10.12.0",
        "openinference-instrumentation-smolagents==0.1.13",
    ]
)