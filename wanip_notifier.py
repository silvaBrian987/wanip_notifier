#!/usr/bin/env python

import os
import subprocess
import logging
import smtplib
import socket
import ssl
import email


class App:
    __logger: logging.Logger = logging.getLogger("ip-notifier")
    __wanip_file: str = os.environ.get(
        "WANIP_FILE", '/tmp/ip-notifier/current.ip')
    __smtp_server: str = os.environ.get("WANIP_SMTP_SERVER")
    __smtp_port: int = int(os.environ.get("WANIP_SMTP_PORT"))
    __smtp_user: str = os.environ.get("WANIP_SMTP_USER")
    __smtp_password: str = os.environ.get("WANIP_SMTP_PASSWORD")
    __send_to: str = os.environ.get("WANIP_SEND_TO")
    __send_from: str = os.environ.get("WANIP_SEND_FROM")

    def run(self) -> None:
        current_ip4 = self.get_current_wanip4()
        self.__logger.debug("current_ip4 = {}".format(current_ip4))
        new_ip4 = self.get_wanip4_from_dns()
        self.__logger.debug("new_ip4 = {}".format(new_ip4))

        if(current_ip4 is None or current_ip4 != new_ip4):
            self.__logger.info(
                f"Cambió la IP! Antes era {current_ip4} y ahora es {new_ip4}")
            self.send_email(new_ip4)
            self.set_wanip4(new_ip4)

    def get_wanip4_from_dns(self) -> str:
        cmd = ["dig", "@resolver1.opendns.com",
               "ANY", "myip.opendns.com", "+short", "-4"]
        process = subprocess.run(cmd,
                                 check=True, stdout=subprocess.PIPE)
        output = process.stdout.decode('UTF-8').strip('\n')
        if 'failed' in output:
            raise ConnectionError(output)
        return output

    def get_current_wanip4(self) -> str:
        if not os.path.exists(self.__wanip_file):
            return None
        with open(self.__wanip_file) as f:
            return f.readline()

    def set_wanip4(self, ip: str) -> None:
        dir = self.__wanip_file[0:self.__wanip_file.rindex('/')]
        if not os.path.exists(dir):
            os.mkdir(dir)
        with open(self.__wanip_file, 'w') as f:
            f.write(ip)

    def send_email(self, ip: str):
        self.__logger.debug("Enviando email...")
        server = socket.gethostname()
        message = f"Esta es la nueva ip del servidor {server}:\n{ip}"
        msg = email.message.EmailMessage()
        msg.set_content(message)
        msg['Subject'] = f"wanip_notifier - Nueva ip para {server}"
        msg['From'] = self.__send_from
        msg['To'] = self.__send_to
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.__smtp_server, self.__smtp_port, context=context) as smtp_server:
            smtp_server.login(self.__smtp_user, self.__smtp_password)
            smtp_server.send_message(msg)
            self.__logger.debug("Email enviado!")


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format=os.environ.get("WANIP_LOG_FORMAT", "%(asctime)s - [%(levelname)s] - %(message)s"))
    App().run()
