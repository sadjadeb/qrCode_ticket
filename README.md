# QR Code Ticket

This service generates a unique qr code for each registered user and also provides a qr reader for the receptionist to verify each ticket powered by Fastapi

## Screenshot

![ticket](ticket.png)

## Getting Started
Clone repository
```bash
git clone https://github.com/sadjadeb/qrCode_ticket.git
```

### Prerequisite
Create an environment to run the app
```bash
cd qrCode_ticket/
sudo apt-get install virtualenv
virtualenv venv
source venv/bin/activate
```
Install required libraries
```bash
pip install -r requirements.txt
```
\
Rename sample_config to config and replace mock data with valid ones

## Run

Run the following command to start the webserver
```bash
python main.py run_webserver
```

Run the following command to add ticket ids and links for registered users
```bash
python main.py generate_ticket_link
```
\
Now open the base url and pass the specified user's ticket_id as a query parameter to see the ticket

For the receptionist, get the /reception endpoint and enter the password to open the QR code reader

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Give a ⭐️ if you like this project!

## License
[MIT](https://github.com/sadjadeb/qrCode_ticket/blob/master/LICENSE)