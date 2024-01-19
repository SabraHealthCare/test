# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <ProgramSnippet>
import asyncio
import configparser
from graph import Graph

import streamlit as st                

import requests
from msal import ConfidentialClientApplication

async def main():
    st.write('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)
    st.write("Graph",Graph)

    greet_user(graph)
    display_access_token(graph)
    list_inbox(graph)
    send_mail(graph)
    make_graph_call(graph)
           


# <GreetUserSnippet>
async def greet_user(graph: Graph):
    user = await graph.get_user()
    if user:
        st.write('Hello,', user.display_name)
        # For Work/school accounts, email is in mail property
        # Personal accounts, email is in userPrincipalName
        st.write('Email:', user.mail or user.user_principal_name, '\n')
# </GreetUserSnippet>

# <DisplayAccessTokenSnippet>
async def display_access_token(graph: Graph):
    token = await graph.get_user_token()
    st.write('User token:', token, '\n')
# </DisplayAccessTokenSnippet>

# <ListInboxSnippet>
async def list_inbox(graph: Graph):
    message_page = await graph.get_inbox()
    if message_page and message_page.value:
        # Output each message's details
        for message in message_page.value:
            st.write('Message:', message.subject)
            if (
                message.from_ and
                message.from_.email_address
            ):
                st.write('  From:', message.from_.email_address.name or 'NONE')
            else:
                st.write('  From: NONE')
            st.write('  Status:', 'Read' if message.is_read else 'Unread')
            st.write('  Received:', message.received_date_time)

        # If @odata.nextLink is present
        more_available = message_page.odata_next_link is not None
        st.write('\nMore messages available?', more_available, '\n')
# </ListInboxSnippet>

# <SendMailSnippet>
async def send_mail(graph: Graph):
    # Send mail to the signed-in user
    # Get the user for their email address
    user = await graph.get_user()
    if user:
        user_email = user.mail or user.user_principal_name

        await graph.send_mail('Testing Microsoft Graph', 'Hello world!', user_email or '')
        st.write('Mail sent.\n')
# </SendMailSnippet>

# <MakeGraphCallSnippet>
async def make_graph_call(graph: Graph):
    await graph.make_graph_call()
# </MakeGraphCallSnippet>

# Run main
asyncio.run(main())
