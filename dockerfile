FROM python:3.11

# Create app directory
WORKDIR /app

# Copy everything over
COPY . .

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./main.py" ]