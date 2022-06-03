FROM python
RUN pip install requests
COPY . /app
ENTRYPOINT [ "python", "-u", "/app/run_workflow.py" ]