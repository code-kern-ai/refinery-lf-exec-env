FROM kernai/refinery-parent-images:python-upgrade-exec-env

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["/run.sh"] 
