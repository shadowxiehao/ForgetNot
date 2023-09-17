import base64

import requests
from django.core import serializers
from itsdangerous import URLSafeTimedSerializer as utsr
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from userApp.models import User, Event, Event_User_Relation


class Adapters:
    adapter_format = "json"

    def __int__(self, adapter_format="json"):
        self.adapter_format = adapter_format

    def serialize(self, obj):
        if len(obj) != 1:
            return serializers.serialize(self.adapter_format, obj, ensure_ascii=False)
        else:
            return serializers.serialize(self.adapter_format, [obj], ensure_ascii=False).replace("[", "").replace("]",
                                                                                                                  "")

    def deserialize(self, string):
        results = []
        if string[0] != "[":
            string = "[" + string + "]"
        for obj in serializers.deserialize(self.adapter_format, string):
            results.append(obj)
        if len(results) != 1:
            return results
        else:
            return results[0]


class MailSender:

    def __init__(self, sender_name="ForgetNot Admin", prefix="admin", ):
        self.sender_name = sender_name
        self.prefix = prefix
        self.API_KEY = '1e75f4fc43cbd984b1c7e2db27b73bb0-15b35dee-533e53e4'
        self.API_base_URL = "https://api.eu.mailgun.net/v3/forgetnot.uk/messages"

    def send_message(self, to_list=None, subject="", text=""):
        if to_list is None:
            to_list = []
        return requests.post(
            self.API_base_URL,
            auth=("api", self.API_KEY),
            data={"from": self.sender_name + " <" + self.prefix + "@forgetnot.uk>",
                  "to": to_list,
                  "subject": subject,
                  "text": text})


def send_verification_code_email(email, verification_code):
    html_content = verify_code(verification_code)
    mailsender = MailSender()
    requests.post(
        mailsender.API_base_URL,
        auth=("api", mailsender.API_KEY),
        data={"from": mailsender.sender_name + " <" + mailsender.prefix + "@forgetnot.uk>",
              "to": email,
              "subject": "Your friend invite you",
              "html": html_content})


def send_invite_email(email, user: User, event: Event, rel: Event_User_Relation):
    html_context = invite_text(event_title=event.title, inviter_name=user.firstName + " " + user.lastName,
                               start_time=event.startDate, end_time=event.endDate, inviter_email=user.email,
                               rel_id=str(rel.id))
    mailsender = MailSender()
    print(requests.post(
        mailsender.API_base_URL,
        auth=("api", mailsender.API_KEY),
        data={"from": mailsender.sender_name + " <" + mailsender.prefix + "@forgetnot.uk>",
              "to": email,
              "subject": "Event invitation",
              "html": html_context}))


def send_contact_email(name, email):
    print(name,email)
    html_context = contact_text(name)
    mailsender = MailSender()
    print(requests.post(
        mailsender.API_base_URL,
        auth=("api", mailsender.API_KEY),
        data={"from": mailsender.sender_name + " <" + mailsender.prefix + "@forgetnot.uk>",
              "to": email,
              "subject": "Thanks for your visit",
              "html": html_context}))


class Token:

    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.b64encode(bytes(security_key, 'utf-8'))

    def generate_validate_token(self, email):
        serializer = utsr(self.security_key)
        return serializer.dumps(email, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token,
                                salt=self.salt,
                                max_age=expiration)


class MyResponse(Response):
    def __init__(self, data=None, msg="", status=HTTP_200_OK, **kwargs):
        result = {}
        if status is not None:
            result['status'] = status
        if msg is not None:
            result['msg'] = msg
        if data is not None:
            result['data'] = data

        super().__init__(data=result, status=status, **kwargs)


def verify_code(verification_code):
    text = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Verification</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;">
        <tr>
            <td align="center" bgcolor="#ffffff" style="padding: 40px 0 30px 0;">
                <img src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB0PSIxNjc5MzY1OTcxMzM3IiBjbGFzcz0iaWNvbiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjQyMjIiIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCI+PHBhdGggZD0iTTMxNS43MzMzMzMgNjc4LjM0ODhjLTguNTMzMzMzLTE4LjY3MDkzMy0zOC4wNDE2LTIzLjUwMDgtNjUuOTk2OC0xMC43ODYxMzNhNzkuODU0OTMzIDc5Ljg1NDkzMyAwIDAgMC0xOC4xNTg5MzMgMTEuMzQ5MzMzIDc5Ljg3MiA3OS44NzIgMCAwIDAgMC4zOTI1MzMtMjEuNDAxNmMtMy40MTMzMzMtMzAuNDk4MTMzLTIyLjgwMTA2Ny01My4zNjc0NjctNDMuMTk1NzMzLTUxLjA0NjRzLTM0LjEzMzMzMyAyOC45MjgtMzAuNzIgNTkuNDI2MTMzYTc5Ljg3MiA3OS44NzIgMCAwIDAgNS4xMiAyMC43NzAxMzQgNzkuODU0OTMzIDc5Ljg1NDkzMyAwIDAgMC0yMC4yNDEwNjctNi45OTczMzRjLTMwLjA4ODUzMy02LjEyNjkzMy01Ny43ODc3MzMgNS4xMi02MS45MDA4IDI1LjI5MjhzMTYuOTY0MjY3IDQxLjM2OTYgNDcuMDUyOCA0Ny41MTM2YTc5Ljg3MiA3OS44NzIgMCAwIDAgMjEuMzUwNCAxLjQ4NDggNzkuODcyIDc5Ljg3MiAwIDAgMC0xMi45MDI0IDE3LjA2NjY2N2MtMTUuMTIxMDY3IDI2LjcwOTMzMy0xMi45MTk0NjcgNTYuNTc2IDQuOTMyMjY3IDY2LjY3OTQ2N3M0NC41OTUyLTMuNDEzMzMzIDU5LjczMzMzMy0zMC4wNzE0NjdhNzkuODcyIDc5Ljg3MiAwIDAgMCA4LjAyMTMzNC0xOS44NDg1MzMgNzkuODcyIDc5Ljg3MiAwIDAgMCAxMi4yNTM4NjYgMTcuNTYxNmMyMC43MzYgMjIuNjQ3NDY3IDQ5LjgwMDUzMyAyOS43NjQyNjcgNjQuOTM4NjY3IDE1LjkwNjEzM3MxMC41OTg0LTQzLjQ1MTczMy0xMC4xMzc2LTY2LjA5OTJhNzkuODU0OTMzIDc5Ljg1NDkzMyAwIDAgMC0xNi40MDEwNjctMTMuNzU1NzMzIDc5Ljg3MiA3OS44NzIgMCAwIDAgMjAuNDgtNi4yMjkzMzRjMjguMTI1ODY3LTEyLjY4MDUzMyA0My45MTI1MzMtMzguMTI2OTMzIDM1LjM3OTItNTYuODE0OTMzeiBtLTEwNC4yMjYxMzMgNjAuOTI4YTI2LjA3Nzg2NyAyNi4wNzc4NjcgMCAwIDAtNi41NTM2IDkuNTQwMjY3IDI1LjYgMjUuNiAwIDAgMC0xOS42MjY2NjctMTEuMTEwNCAyNS42IDI1LjYgMCAwIDAgNC41MDU2LTIyLjEwMTMzNCAyNS42IDI1LjYgMCAwIDAgMjIuNDA4NTM0LTIuNTQyOTMzIDI1LjYgMjUuNiAwIDAgMCA5LjMzNTQ2NiAyMC40OCAyNi4wNzc4NjcgMjYuMDc3ODY3IDAgMCAwLTEwLjA1MjI2NiA1LjczNDR6IiBmaWxsPSIjRDUzODJFIiBwLWlkPSI0MjIzIj48L3BhdGg+PHBhdGggZD0iTTE1NC42NzUyIDg0Ni4xNDgyNjdhMzEuMTYzNzMzIDMxLjE2MzczMyAwIDAgMS0xNS41MzA2NjctMy45NTk0NjdjLTIwLjI3NTItMTEuNDg1ODY3LTIzLjM2NDI2Ny00NC41MjY5MzMtNi44MjY2NjYtNzMuNjU5NzMzYTg3LjUzNDkzMyA4Ny41MzQ5MzMgMCAwIDEgNi4xOTUyLTkuNDg5MDY3IDg3LjcyMjY2NyA4Ny43MjI2NjcgMCAwIDEtMTEuMjI5ODY3LTEuNTUzMDY3Yy0xNS41MzA2NjctMy4xNzQ0LTI5LjM3MTczMy0xMC4yNC0zOC45NjMyLTE5LjkzMzg2Ni0xMC4xMjA1MzMtMTAuMjQtMTQuNDIxMzMzLTIyLjE4NjY2Ny0xMi4wODMyLTMzLjYyMTMzNHMxMC45NTY4LTIwLjc1MzA2NyAyNC4yODU4NjctMjYuMjE0NGMxMi42MTIyNjctNS4xMiAyOC4xMDg4LTYuMjYzNDY3IDQzLjY1NjUzMy0zLjA4OTA2NmE4Ny44MDggODcuODA4IDAgMCAxIDEwLjg4ODUzMyAyLjkxODQgODcuNDMyNTMzIDg3LjQzMjUzMyAwIDAgMS0xLjk5NjgtMTEuMTQ0NTM0Yy0zLjc3MTczMy0zMy4yNjI5MzMgMTEuOTQ2NjY3LTYyLjQ2NCAzNS4xNTczMzQtNjUuMDkyMjY2czQ1LjA3MzA2NyAyMi4yODkwNjcgNDguODYxODY2IDU1LjU1MmE4Ny40ODM3MzMgODcuNDgzNzMzIDAgMCAxIDAuNTYzMiAxMS4zMTUyIDg3LjY3MTQ2NyA4Ny42NzE0NjcgMCAwIDEgOS45ODQtNS4zNDE4NjdjMTQuNDIxMzMzLTYuNTcwNjY3IDI5Ljc4MTMzMy04Ljk3NzA2NyA0My4yMjk4NjctNi44MjY2NjcgMTQuMTk5NDY3IDIuMzIxMDY3IDI0LjY5NTQ2NyA5LjQ1NDkzMyAyOS41NDI0IDIwLjEwNDUzNHMzLjQxMzMzMyAyMy4yMjc3MzMtNC4yMzI1MzMgMzUuNDgxNmMtNy4xNjggMTEuNTg4MjY3LTE5LjA2MzQ2NyAyMS41ODkzMzMtMzMuNTAxODY3IDI4LjE2YTg3Ljc5MDkzMyA4Ny43OTA5MzMgMCAwIDEtMTAuNTk4NCA0LjAyNzczMyA4Ny44NTkyIDg3Ljg1OTIgMCAwIDEgOC4xNzQ5MzMgNy44NTA2NjdjMTAuNzAwOCAxMS42OTA2NjcgMTcuNzMyMjY3IDI1LjYgMTkuNzk3MzM0IDM5LjAxNDQgMi4xODQ1MzMgMTQuMjMzNi0xLjM2NTMzMyAyNi40MDIxMzMtOS45ODQgMzQuMzA0LTE3LjE4NjEzMyAxNS43MzU0NjctNDkuNDkzMzMzIDguNTMzMzMzLTcyLjE3NDkzNC0xNi4yMzA0YTg3Ljk2MTYgODcuOTYxNiAwIDAgMS03LjA5OTczMy04LjgyMzQ2NyA4Ny43MjI2NjcgODcuNzIyNjY3IDAgMCAxLTQuOTQ5MzMzIDEwLjI0Yy0xMi42MjkzMzMgMjIuMzc0NC0zMy4xNDM0NjcgMzYuMDEwNjY3LTUxLjE2NTg2NyAzNi4wMTA2Njd6IG04LjI0MzItOTguMjE4NjY3bC05LjY1OTczMyA5LjY1OTczM2E3NC41MzAxMzMgNzQuNTMwMTMzIDAgMCAwLTEyLjA2NjEzNCAxNS45OTE0NjdjLTEzLjY1MzMzMyAyNC4yMTc2LTEyLjM3MzMzMyA1MC45OTUyIDMuMDAzNzM0IDU5LjczMzMzM3MzOS4wMzE0NjctMy45MDgyNjcgNTIuNzUzMDY2LTI4LjEyNTg2NmE3NC41MzAxMzMgNzQuNTMwMTMzIDAgMCAwIDcuNTA5MzM0LTE4LjU2ODUzNGwzLjMyOC0xMy4yNDM3MzMgNi4yMTIyNjYgMTIuMTY4NTMzYTc0LjQ5NiA3NC40OTYgMCAwIDAgMTEuNDY4OCAxNi40MTgxMzRjMTguNzczMzMzIDIwLjQ4IDQ0LjY4MDUzMyAyNy41MTE0NjcgNTcuNzAyNCAxNS41OTg5MzMgNi4wMjQ1MzMtNS41MTI1MzMgOC40MzA5MzMtMTQuNDU1NDY3IDYuODI2NjY3LTI1LjE5MDQtMS43MDY2NjctMTEuNDg1ODY3LTcuODg0OC0yMy40NDk2LTE3LjIzNzMzMy0zMy42NTU0NjdhNzQuNTY0MjY3IDc0LjU2NDI2NyAwIDAgMC0xNS4zNi0xMi44NjgyNjZsLTExLjYzOTQ2Ny03LjMyMTYgMTMuNDgyNjY3LTIuMTUwNGE3NC41NjQyNjcgNzQuNTY0MjY3IDAgMCAwIDE5LjE2NTg2Ni01LjgzNjhjMTIuNTk1Mi01LjczNDQgMjIuOTIwNTMzLTE0LjMzNiAyOS4wMTMzMzQtMjQuMjE3NiA1LjcxNzMzMy05LjIzMzA2NyA3LjAxNDQtMTguNDE0OTMzIDMuNjE4MTMzLTI1LjgzODkzNC0zLjQxMzMzMy03LjQyNC0xMS4xNDQ1MzMtMTIuNDc1NzMzLTIxLjg2MjQtMTQuMjMzNi0xMS40Njg4LTEuODc3MzMzLTI0LjcyOTYgMC4yNTYtMzcuMzQxODY3IDUuOTkwNGE3NC41NDcyIDc0LjU0NzIgMCAwIDAtMTcuMDY2NjY2IDEwLjYxNTQ2N2wtMTAuNDc4OTM0IDguNzcyMjY3IDIuMTMzMzM0LTEzLjQ4MjY2N2E3NC43MzQ5MzMgNzQuNzM0OTMzIDAgMCAwIDAuNTYzMi0yMC4wNTMzMzNjLTMuMTQwMjY3LTI3LjY0OC0xOS45NjgtNDguNTIwNTMzLTM3LjU0NjY2Ny00Ni41NDA4cy0yOS4yNjkzMzMgMjYuMTEyLTI2LjE0NjEzMyA1My43NmE3NC42NjY2NjcgNzQuNjY2NjY3IDAgMCAwIDQuODQ2OTMzIDE5LjQzODkzM2w1LjEyIDEyLjY2MzQ2Ny0xMi4yMzY4LTYuMjEyMjY3YTc0LjUzMDEzMyA3NC41MzAxMzMgMCAwIDAtMTguOTI2OTMzLTYuNTM2NTMzYy0xMy41NjgtMi43NjQ4LTI2Ljk2NTMzMy0xLjg2MDI2Ny0zNy43MzQ0IDIuNTI1ODY2LTEwLjA1MjI2NyA0LjExMzA2Ny0xNi40ODY0IDEwLjc4NjEzMy0xOC4xMjQ4IDE4Ljc3MzMzNHMxLjcwNjY2NyAxNi42NTcwNjcgOS4zMTg0IDI0LjM3MTJjOC4xNzQ5MzMgOC4yNjAyNjcgMjAuMTU1NzMzIDE0LjMzNiAzMy43MjM3MzMgMTcuMDY2NjY2YTc0LjUxMzA2NyA3NC41MTMwNjcgMCAwIDAgMTkuOTg1MDY3IDEuMzk5NDY3eiBtNDMuMjY0IDExLjUzNzA2N2wtNS40MTAxMzMtNy42OTcwNjdhMjAuNDggMjAuNDggMCAwIDAtMTUuNzg2NjY3LTguOTQyOTMzbC05LjM4NjY2Ny0wLjY2NTYgNS42NjYxMzQtNy41MjY0YTIwLjQ4IDIwLjQ4IDAgMCAwIDMuNjE4MTMzLTE3LjgzNDY2N2wtMi4yNjk4NjctOS4wNzk0NjcgOC45MDg4IDMuMDU0OTM0YTIwLjQ4IDIwLjQ4IDAgMCAwIDE4LjAzOTQ2Ny0yLjA0OGw3Ljk4NzItNC45ODM0NjctMC4xNTM2IDkuNDAzNzMzYTIwLjQ4IDIwLjQ4IDAgMCAwIDcuNTI2NCAxNi41MjA1MzRsNy4xODUwNjcgNi4wNzU3MzMtOC45OTQxMzQgMi43NDc3MzNhMjEuMDI2MTMzIDIxLjAyNjEzMyAwIDAgMC04LjEyMzczMyA0LjU3Mzg2NyAyMC45OTIgMjAuOTkyIDAgMCAwLTUuMjU2NTMzIDcuNjk3MDY3eiBtLTEyLjgzNDEzMy0yNS4zOTUyYTMwLjMxMDQgMzAuMzEwNCAwIDAgMSAxMC42MzI1MzMgNi4wMjQ1MzMgMzAuMjA4IDMwLjIwOCAwIDAgMSA0LjA3ODkzMy00LjU5MDkzMyAzMC4zMjc0NjcgMzAuMzI3NDY3IDAgMCAxIDQuOTMyMjY3LTMuNjY5MzM0IDMwLjMyNzQ2NyAzMC4zMjc0NjcgMCAwIDEtNS4xMi0xMS4xMTA0IDMwLjMxMDQgMzAuMzEwNCAwIDAgMS0xMi4xMzQ0IDEuMzgyNCAzMC4yNzYyNjcgMzAuMjc2MjY3IDAgMCAxLTIuNDQwNTMzIDExLjk0NjY2N3oiIGZpbGw9IiNFOEQ0QUIiIHAtaWQ9IjQyMjQiPjwvcGF0aD48cGF0aCBkPSJNMjUxLjQyNjEzMyAyNTUuMDk1NDY3djU5MC42NDMyaDU0OC45MTUyVjI1NS4wOTU0NjdIMjUxLjQyNjEzM3oiIGZpbGw9IiM5OTZFMjgiIHAtaWQ9IjQyMjUiPjwvcGF0aD48cGF0aCBkPSJNMjU4LjI1MjggNDAwLjU4ODhoNTM1LjI0NDh2NDIxLjI1NjUzM0gyNTguMjUyOHoiIGZpbGw9IiNENTM4MkUiIHAtaWQ9IjQyMjYiIGRhdGEtc3BtLWFuY2hvci1pZD0iYTMxM3guNzc4MTA2OS4wLmk1IiBjbGFzcz0ic2VsZWN0ZWQiPjwvcGF0aD48cGF0aCBkPSJNODAwLjM0MTMzMyA4MjguNjcySDI1MS40NDMyVjM5My43NjIxMzNoNTQ4Ljg5ODEzM3ogbS01MzUuMjQ0OC0xMy42NTMzMzNoNTIxLjU5MTQ2N1Y0MDcuNDE1NDY3SDI2NS4wOTY1MzN6IiBmaWxsPSIjRThENEFCIiBwLWlkPSI0MjI3IiBkYXRhLXNwbS1hbmNob3ItaWQ9ImEzMTN4Ljc3ODEwNjkuMC5pNiIgY2xhc3M9InNlbGVjdGVkIj48L3BhdGg+PHBhdGggZD0iTTU4MS45NzMzMzMgNjA3LjQwMjY2N2MxNS41NDc3MzMtMTIuNzE0NjY3IDI1LjI3NTczMy0zMC42MTc2IDI1LjI3NTczNC01MC40NjYxMzQgMC0zOC40NTEyLTM2LjQ3MTQ2Ny02OS43MzQ0LTgxLjMyMjY2Ny02OS43MzQ0cy04MS4zMjI2NjcgMzEuMjgzMi04MS4zMjI2NjcgNjkuNzM0NGMwIDE5LjgzMTQ2NyA5LjcyOCAzNy43NTE0NjcgMjUuMjc1NzM0IDUwLjQ2NjEzNC0yNS45MDcyIDE1LjIwNjQtNDIuOTIyNjY3IDQwLjYxODY2Ny00Mi45MjI2NjcgNjkuMzQxODY2IDAgNDYuNDIxMzMzIDQ0LjM3MzMzMyA4NC4yMDY5MzMgOTguOTg2NjY3IDg0LjIwNjkzNHM5OC45ODY2NjctMzcuNzY4NTMzIDk4Ljk4NjY2Ni04NC4yMDY5MzRjLTAuMDg1MzMzLTI4Ljc0MDI2Ny0xNy4xMDA4LTU0LjE1MjUzMy00Mi45NTY4LTY5LjM0MTg2NnogbS0xMjAuODY2MTMzIDY5LjM0MTg2NmMwLTI3LjYxMzg2NyAyOS4wMTMzMzMtNTAuMDczNiA2NC44NTMzMzMtNTAuMDczNnM2NC44NTMzMzMgMjIuNDU5NzMzIDY0Ljg1MzMzNCA1MC4wNzM2LTI5LjAxMzMzMyA1MC4wNzM2LTY0Ljg1MzMzNCA1MC4wNzM2LTY0LjkwNDUzMy0yMi40NTk3MzMtNjQuOTA0NTMzLTUwLjA3MzZ6IG0xNy42NDY5MzMtMTE5LjgwOGMwLTE5LjYyNjY2NyAyMS4xNjI2NjctMzUuNjAxMDY3IDQ3LjE4OTMzNC0zNS42MDEwNjZzNDcuMTg5MzMzIDE1Ljk3NDQgNDcuMTg5MzMzIDM1LjYwMTA2Ni0yMS4xNjI2NjcgMzUuNjAxMDY3LTQ3LjE4OTMzMyAzNS42MDEwNjctNDcuMjQwNTMzLTE1Ljk3NDQtNDcuMjQwNTM0LTM1LjYwMTA2N3oiIGZpbGw9IiM2MzFCMUIiIHAtaWQ9IjQyMjgiPjwvcGF0aD48cGF0aCBkPSJNMjU4LjI1MjggMjQ0Ljg1NTQ2N2g1MzUuMjQ0OHYxNDQuMDI1NkgyNTguMjUyOHoiIGZpbGw9IiNBRjMxMzEiIHAtaWQ9IjQyMjkiPjwvcGF0aD48cGF0aCBkPSJNODAwLjM0MTMzMyAzOTUuNzA3NzMzSDI1MS40NDMydi0xNTcuNjc4OTMzaDU0OC44OTgxMzN6IG0tNTM1LjI0NDgtMTMuNjUzMzMzaDUyMS41OTE0Njd2LTEzMC4zNzIyNjdIMjY1LjA5NjUzM3oiIGZpbGw9IiNFOEQ0QUIiIHAtaWQ9IjQyMzAiPjwvcGF0aD48cGF0aCBkPSJNODc5Ljk0MDI2NyAxMjYuNjg1ODY3Yy0xOS42OTQ5MzMtMTAuMDM1Mi00Ny43ODY2NjcgNS43MTczMzMtNjIuODIyNCAzNS4xNzQ0YTg1Ljk5ODkzMyA4NS45OTg5MzMgMCAwIDAtNy42OCAyMS43NDI5MzMgODUuOTk4OTMzIDg1Ljk5ODkzMyAwIDAgMC0xNC4wMjg4LTE4LjI5NTQ2N2MtMjMuMzgxMzMzLTIzLjM4MTMzMy01NC45ODg4LTI5LjY2MTg2Ny03MC42MjE4NjctMTQuMDQ1ODY2cy05LjMzNTQ2NyA0Ny4yNDA1MzMgMTQuMDQ1ODY3IDcwLjYyMTg2NmE4NS45OTg5MzMgODUuOTk4OTMzIDAgMCAwIDE4LjI5NTQ2NiAxNC4wMjg4IDg1Ljk5ODkzMyA4NS45OTg5MzMgMCAwIDAtMjEuNzQyOTMzIDcuNjhjLTI5LjQ1NzA2NyAxNS4wMDE2LTQ1LjIwOTYgNDMuMTQ0NTMzLTM1LjE3NDQgNjIuODIyNHM0Mi4wMzUyIDIzLjQ4MzczMyA3MS40OTIyNjcgOC41MzMzMzRhODYuMDE2IDg2LjAxNiAwIDAgMCAxOC45OTUyLTEzLjA3MzA2NyA4NS45OTg5MzMgODUuOTk4OTMzIDAgMCAwIDAuNTgwMjY2IDIzLjA0YzUuMTIgMzIuNjQ4NTMzIDI3LjA1MDY2NyA1Ni4zMiA0OC44Nzg5MzQgNTIuOTA2NjY3Uzg3NS41MiAzNDQuOTg1NiA4NzAuNCAzMTIuMzJhODUuOTk4OTMzIDg1Ljk5ODkzMyAwIDAgMC02LjU3MDY2Ny0yMi4xMDEzMzMgODUuOTk4OTMzIDg1Ljk5ODkzMyAwIDAgMCAyMi4xMDEzMzQgNi41NzA2NjZjMzIuNjQ4NTMzIDUuMTIgNjEuOTE3ODY3LTguMzI4NTMzIDY1LjM4MjQtMzAuMTU2OHMtMjAuMjA2OTMzLTQzLjcwNzczMy01Mi45MDY2NjctNDguODc4OTMzYTg1Ljk5ODkzMyA4NS45OTg5MzMgMCAwIDAtMjMuMDQtMC41ODAyNjcgODYuMDE2IDg2LjAxNiAwIDAgMCAxMy4wNzMwNjctMTguOTk1MmMxNC45ODQ1MzMtMjkuNDQgMTEuMTk1NzMzLTYxLjQ1NzA2Ny04LjQ5OTItNzEuNDkyMjY2eiBtLTQ2LjkzMzMzNCAxMjEuMTczMzMzYTI4LjA3NDY2NyAyOC4wNzQ2NjcgMCAwIDAgMC44ODc0NjcgMTIuNDI0NTMzIDI3LjU5NjggMjcuNTk2OCAwIDAgMC0yMy45Nzg2NjcgMy44MDU4NjcgMjcuNTk2OCAyNy41OTY4IDAgMCAwLTExLjAyNTA2Ni0yMS42NDA1MzNBMjcuNTk2OCAyNy41OTY4IDAgMCAwIDgxNi4wNDI2NjcgMjI1LjI4YTI3LjU5NjggMjcuNTk2OCAwIDAgMCAyMS42NDA1MzMgMTEuMDI1MDY3IDI4LjA3NDY2NyAyOC4wNzQ2NjcgMCAwIDAtNC42NzYyNjcgMTEuNjIyNHoiIGZpbGw9IiNENTM4MkUiIHAtaWQ9IjQyMzEiPjwvcGF0aD48cGF0aCBkPSJNODM1Ljg1NzA2NyAzODMuMTgwOGMtMTAuNTk4NCAwLTIxLjE0NTYtNS4xMi0zMC4xMjI2NjctMTQuODgyMTMzLTkuOTE1NzMzLTEwLjcxNzg2Ny0xNi44Mjc3MzMtMjUuODczMDY3LTE5LjQ5MDEzMy00Mi42NjY2NjdhOTMuODY2NjY3IDkzLjg2NjY2NyAwIDAgMS0xLjE0MzQ2Ny0xMi44MTcwNjcgOTMuODY2NjY3IDkzLjg2NjY2NyAwIDAgMS0xMS4wNDIxMzMgNi42MDQ4Yy0xNS4xMzgxMzMgNy43MTQxMzMtMzEuNDcwOTMzIDExLjAwOC00NS45NjA1MzQgOS4zMDEzMzQtMTUuMjU3Ni0xLjgwOTA2Ny0yNi43Nzc2LTguOTA4OC0zMi40MjY2NjYtMjAuMDAyMTM0cy00LjYyNTA2Ny0yNC41OTMwNjcgMi44NjcyLTM3Ljk5MDRjNy4xMzM4NjctMTIuNzMxNzMzIDE5LjQwNDgtMjMuOTk1NzMzIDM0LjU0MjkzMy0zMS43MDk4NjZhOTMuODY2NjY3IDkzLjg2NjY2NyAwIDAgMSAxMS44NDQyNjctNS4xMiA5My42Mjc3MzMgOTMuNjI3NzMzIDAgMCAxLTkuNjkzODY3LTguNTMzMzM0Yy0xMS45NDY2NjctMTEuOTQ2NjY3LTIwLjIwNjkzMy0yNi41MjE2LTIzLjA0LTQwLjg0MDUzMy0zLjAwMzczMy0xNS4wNjk4NjcgMC4yMDQ4LTI4LjIxMTIgOS4wMTEyLTM3LjAxNzYgMTcuNTk1NzMzLTE3LjU5NTczMyA1Mi41MzEyLTExLjI5ODEzMyA3Ny44NTgxMzMgMTQuMDQ1ODY3YTkzLjczMDEzMyA5My43MzAxMzMgMCAwIDEgOC41MzMzMzQgOS42OTM4NjYgOTMuODY2NjY3IDkzLjg2NjY2NyAwIDAgMSA1LjEyLTExLjg0NDI2NmMxNi4xMTA5MzMtMzEuNzc4MTMzIDQ3LjQ0NTMzMy00OC41NzE3MzMgNjkuNjMyLTM3LjI3MzYgMTEuMDkzMzMzIDUuNjQ5MDY3IDE4LjE5MzA2NyAxNy4xNjkwNjcgMjAuMDAyMTMzIDMyLjQyNjY2NiAxLjcwNjY2NyAxNC41MDY2NjctMS41ODcyIDMwLjgyMjQtOS4zMDEzMzMgNDUuOTYwNTM0YTkzLjg2NjY2NyA5My44NjY2NjcgMCAwIDEtNi42MDQ4IDExLjA0MjEzMyA5My44NjY2NjcgOTMuODY2NjY3IDAgMCAxIDEyLjgxNzA2NiAxLjE0MzQ2N2MxNi43NzY1MzMgMi42NjI0IDMxLjkzMTczMyA5LjU3NDQgNDIuNjY2NjY3IDE5LjQ5MDEzMyAxMS4yODEwNjcgMTAuNDI3NzMzIDE2LjQxODEzMyAyMi45NTQ2NjcgMTQuNDcyNTMzIDM1LjI0MjY2Ny0zLjg5MTIgMjQuNTc2LTM1Ljg0IDQwLjAyMTMzMy03MS4yMzYyNjYgMzQuNDA2NGE5My44NjY2NjcgOTMuODY2NjY3IDAgMCAxLTEyLjU0NC0yLjg2NzIgOTMuNjk2IDkzLjY5NiAwIDAgMSAyLjg2NzIgMTIuNTQ0YzUuNTk3ODY3IDM1LjM5NjI2Ny05LjgzMDQgNjcuMzQ1MDY3LTM0LjQwNjQgNzEuMjM2MjY2YTMyLjc2OCAzMi43NjggMCAwIDEtNS4yMjI0IDAuNDI2NjY3eiBtLTM4LjUxOTQ2Ny05NC4zNzg2NjdsLTEuNTM2IDEzLjY1MzMzNGE4MC42MjI5MzMgODAuNjIyOTMzIDAgMCAwIDAuNTQ2MTMzIDIxLjY3NDY2NmMyLjMzODEzMyAxNC43OTY4IDguMzQ1NiAyOC4wNTc2IDE2Ljg5NiAzNy4yOTA2NjcgOC4wMzg0IDguNjg2OTMzIDE3LjMwNTYgMTIuNzE0NjY3IDI2LjEyOTA2NyAxMS4zMTUyIDE4Ljk5NTItMy4wMDM3MzMgMzAuNjE3Ni0yOS43MTMwNjcgMjUuODkwMTMzLTU5LjUyODUzM2E4MC43NTk0NjcgODAuNzU5NDY3IDAgMCAwLTYuMTYxMDY2LTIwLjc4NzJsLTUuNjQ5MDY3LTEyLjUyNjkzNCAxMi40NDE2IDUuNjQ5MDY3YTgwLjY3NDEzMyA4MC42NzQxMzMgMCAwIDAgMjAuNzg3MiA2LjE2MTA2N2MyOS43OTg0IDQuNzI3NDY3IDU2LjUwNzczMy02LjgyNjY2NyA1OS41Mjg1MzMtMjUuODkwMTM0IDEuMzk5NDY3LTguODA2NC0yLjYyODI2Ny0xOC4wOTA2NjctMTEuMzE1Mi0yNi4xMjkwNjYtOS4yNTAxMzMtOC41MzMzMzMtMjIuNDkzODY3LTE0LjU1Nzg2Ny0zNy4zMDc3MzMtMTYuODk2YTgwLjY1NzA2NyA4MC42NTcwNjcgMCAwIDAtMjEuNjc0NjY3LTAuNTYzMmwtMTMuNjUzMzMzIDEuNTM2IDkuMjE2LTEwLjA4NjRhODAuNzQyNCA4MC43NDI0IDAgMCAwIDEyLjI4OC0xNy44NTE3MzRjNi44MjY2NjctMTMuMzQ2MTMzIDkuNzI4LTI3LjU5NjggOC4yNjAyNjctNDAuMTA2NjY2LTEuMzk5NDY3LTExLjc1ODkzMy02LjUzNjUzMy0yMC40OC0xNC40ODk2LTI0LjUwNzczNC0xNy4wNjY2NjctOC43MzgxMzMtNDIuMjQgNi4wNDE2LTU1Ljk0NDUzNCAzMi45Mzg2NjdhODAuNjkxMiA4MC42OTEyIDAgMCAwLTcuMjE5MiAyMC40OGwtMi43MzA2NjYgMTMuMzgwMjY3LTYuNzQxMzM0LTExLjk0NjY2N0E4MC43MDgyNjcgODAuNzA4MjY3IDAgMCAwIDc5MS43OTA5MzMgMTY4Ljk2Yy0yMS4zNTA0LTIxLjM1MDQtNDkuNzgzNDY3LTI3LjY0OC02My4zODU2LTE0LjA0NTg2Ny02LjMxNDY2NyA2LjMxNDY2Ny04LjUzMzMzMyAxNi4xNzkyLTYuMjEyMjY2IDI3Ljc4NDUzNCAyLjQ1NzYgMTIuMzU2MjY3IDkuNjQyNjY3IDI1LjAwMjY2NyAyMC4yNDEwNjYgMzUuNjAxMDY2YTgwLjY5MTIgODAuNjkxMiAwIDAgMCAxNy4yMDMyIDEzLjE5MjUzNGwxMS45NDY2NjcgNi43NDEzMzMtMTMuMzgwMjY3IDIuNzMwNjY3YTgwLjY1NzA2NyA4MC42NTcwNjcgMCAwIDAtMjAuNDggNy4yMTkyYy0xMy4zNjMyIDYuODI2NjY3LTI0LjA5ODEzMyAxNi42MDU4NjctMzAuMjU5MiAyNy41OTY4LTUuNzg1NiAxMC4zMjUzMzMtNi43NDEzMzMgMjAuMzk0NjY3LTIuNjc5NDY2IDI4LjM0NzczM3MxMi43NDg4IDEzLjA5MDEzMyAyNC41MDc3MzMgMTQuNDg5NmMxMi41MDk4NjcgMS40ODQ4IDI2Ljc2MDUzMy0xLjQ1MDY2NyA0MC4xMDY2NjctOC4yNjAyNjdhODAuNjU3MDY3IDgwLjY1NzA2NyAwIDAgMCAxNy44NTE3MzMtMTIuMjg4eiBtNy42OTcwNjctMTUuMTA0bC0wLjI1Ni05LjQwMzczM2EyMi40NzY4IDIyLjQ3NjggMCAwIDAtOS4wMjgyNjctMTcuNzE1MmwtNy40NTgxMzMtNS43MzQ0IDguODc0NjY2LTMuMTQwMjY3YTIyLjQ3NjggMjIuNDc2OCAwIDAgMCAxNC4wNjI5MzQtMTQuMDYyOTMzbDMuMTQwMjY2LTguODc0NjY3IDUuNzM0NCA3LjQ1ODEzNGEyMi40OTM4NjcgMjIuNDkzODY3IDAgMCAwIDE3LjcxNTIgOS4wMjgyNjZsOS40MDM3MzQgMC4yNTYtNS4zMjQ4IDcuNzY1MzM0YTIzLjAyMjkzMyAyMy4wMjI5MzMgMCAwIDAtMy44NCA5LjQ1NDkzMyAyMy4wNCAyMy4wNCAwIDAgMCAwLjczMzg2NiAxMC4yNEw4NDEuMzg2NjY3IDI2Ny45NDY2NjdsLTkuMDI4MjY3LTIuNjYyNGEyMi40NzY4IDIyLjQ3NjggMCAwIDAtMTkuNjQzNzMzIDMuMTA2MTMzeiBtMi42MTEyLTI5Ljc5ODRhMzIuMjU2IDMyLjI1NiAwIDAgMSA2LjI4MDUzMyAxMi4zMzkyIDMyLjI1NiAzMi4yNTYgMCAwIDEgMTMuNjUzMzMzLTIuMTY3NDY2IDMyLjIzODkzMyAzMi4yMzg5MzMgMCAwIDEgMC4zNDEzMzQtNi45NDYxMzQgMzIuMjM4OTMzIDMyLjIzODkzMyAwIDAgMSAxLjgyNjEzMy02LjcyNDI2NiAzMi4yNzMwNjcgMzIuMjczMDY3IDAgMCAxLTEyLjMzOTItNi4yODA1MzQgMzIuMjM4OTMzIDMyLjIzODkzMyAwIDAgMS05Ljc5NjI2NyA5Ljc5NjI2N3pNNTI1Ljg5MjI2NyA2MTkuODQ0MjY3Yy00NC44MzQxMzMgMC04MS4zMjI2NjctMzEuMjgzMi04MS4zMjI2NjctNjkuNzM0NHMzNi40NzE0NjctNjkuNzM0NCA4MS4zMjI2NjctNjkuNzM0NCA4MS4zMDU2IDMxLjI4MzIgODEuMzA1NiA2OS43MzQ0LTM2LjQ3MTQ2NyA2OS43MzQ0LTgxLjMwNTYgNjkuNzM0NHogbTAtMTA1LjMzNTQ2N2MtMjYuMDA5NiAwLTQ3LjE4OTMzMyAxNS45NzQ0LTQ3LjE4OTMzNCAzNS42MDEwNjdzMjEuMTYyNjY3IDM1LjYwMTA2NyA0Ny4xODkzMzQgMzUuNjAxMDY2IDQ3LjE3MjI2Ny0xNS45NzQ0IDQ3LjE3MjI2Ni0zNS42MDEwNjYtMjEuMTYyNjY3LTM1LjYwMTA2Ny00Ny4xNzIyNjYtMzUuNjAxMDY3eiIgZmlsbD0iI0U4RDRBQiIgcC1pZD0iNDIzMiI+PC9wYXRoPjxwYXRoIGQ9Ik01MjUuODkyMjY3IDc1NC4xMjQ4Yy01NC42MTMzMzMgMC05OC45ODY2NjctMzcuNzY4NTMzLTk4Ljk4NjY2Ny04NC4yMDY5MzNzNDQuMzczMzMzLTg0LjIwNjkzMyA5OC45ODY2NjctODQuMjA2OTM0IDk4Ljk4NjY2NyAzNy43Njg1MzMgOTguOTg2NjY2IDg0LjIwNjkzNC00NC40MjQ1MzMgODQuMjA2OTMzLTk4Ljk4NjY2NiA4NC4yMDY5MzN6IG0wLTEzNC4yNjM0NjdjLTM1LjczNzYgMC02NC44NTMzMzMgMjIuNDU5NzMzLTY0Ljg1MzMzNCA1MC4wNzM2czI5LjAxMzMzMyA1MC4wNzM2IDY0Ljg1MzMzNCA1MC4wNzM2IDY0Ljg1MzMzMy0yMi40NTk3MzMgNjQuODUzMzMzLTUwLjA3MzYtMjkuMTE1NzMzLTUwLjA5MDY2Ny02NC44NTMzMzMtNTAuMDkwNjY2eiIgZmlsbD0iI0U4RDRBQiIgcC1pZD0iNDIzMyIgZGF0YS1zcG0tYW5jaG9yLWlkPSJhMzEzeC43NzgxMDY5LjAuaTciPjwvcGF0aD48L3N2Zz4=" alt="Your Logo" width="200" style="display: block;" />
            </td>
        </tr>
        <tr>
            <td bgcolor="#f0f2f5" style="padding: 40px 30px 40px 30px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td style="color: #153643; font-size: 24px;">
                            <b>Email Verification</b>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 20px 0 30px 0; color: #153643; font-size: 16px; line-height: 24px;">
                            Thank you for registering on our website. To verify your email address, please enter the following 6-digit verification code:
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 0 10px 0; color: #153643; font-size: 28px; font-weight: bold;">
                            {verification_code}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 30px 0 20px 0; color: #153643; font-size: 16px; line-height: 24px;">
                            If you didn't request this email or suspect any suspicious activity, please contact our support team immediately.
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td bgcolor="#007bff" style="padding: 30px 30px 30px 30px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                        <td style="color: #ffffff; font-size: 14px;">
                            &copy; Your Company Name. All rights reserved.
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    return text


def invite_text(event_title, inviter_name, start_time, end_time, inviter_email, rel_id):
    text = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Invitation Letter</title>
  </head>
  <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
    <table style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #f0f2f5;">
      <tr>
        <td style="padding: 40px 30px 40px 30px;">
          <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
              <td style="color: #153643; font-size: 24px;">
                <b>Invitation to {event_title}</b>
              </td>
            </tr>
            <tr>
              <td style="padding: 20px 0 30px 0; color: #153643; font-size: 16px; line-height: 24px;">
                You have been invited to attend {event_title} by {inviter_name}. The details of the event are as follows:
              </td>
            </tr>
            <tr>
              <td style="padding: 10px 0 10px 0; color: #153643; font-size: 16px; line-height: 24px;">
                <b>Event:</b> {event_title}<br>
                <b>Start Time:</b> {start_time}<br>
                <b>End Time:</b> {end_time}<br>
                <b>Reference Number:</b>{rel_id}<br>
              </td>
            </tr>
            <tr>
              <td style="padding: 30px 0 20px 0; color: #153643; font-size: 16px; line-height: 24px;">
                You can also check the details with the Reference number in the https://forgetnot.uk.
                Please click on the button below to accept or reject this invitation. Your response will be sent to {inviter_email}.
              </td>
            </tr>
            <tr>
              <td>
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tr>
                    <td style="padding: 10px;">
                      <a href="{"https://forgetnot.uk/api/invite/accept/?ref_id=" + rel_id}" style="display: block; width: 200px; height: 40px; background-color: #4CAF50; color: #fff; text-align: center; text-decoration: none; line-height: 40px; font-weight: bold; border-radius: 4px;">Accept</a>
                    </td>
                    <td style="padding: 10px;">
                      <a href="{"https://forgetnot.uk/api/invite/reject/?ref_id=" + rel_id}" style="display: block; width: 200px; height: 40px; background-color: #f44336; color: #fff; text-align: center; text-decoration: none; line-height: 40px; font-weight: bold; border-radius: 4px;">Reject</a>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
    """
    return text


def contact_text(name):
    text = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Thank you for contacting us</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="background-color: #f0f2f5; font-family: Arial, sans-serif; font-size: 16px; line-height: 24px; margin: 0; padding: 0;">
        <table style="background-color: #ffffff; border-collapse: collapse; border-spacing: 0; margin: 0 auto; max-width: 600px; width: 100%;">
            <tr>
                <td style="padding: 40px 30px 40px 30px;">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td style="color: #153643; font-size: 24px; font-weight: bold; text-align: center;">
                                Dear {name},
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 20px 0 30px 0; color: #153643; font-size: 16px; line-height: 24px;">
                                Thank you for contacting us! We have received your question and will reply to you as soon as possible.
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
"""
    return text
