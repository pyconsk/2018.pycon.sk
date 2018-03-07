# OpenPGP Key Signing Party

This year we are introducing the [PyConSK OpenPGP Key-signing party](https://2018.pycon.sk/en/friday/schedule.html)! This involves meeting people to verify their online cryptographic identities in person. Read more on [the Wikipedia page about key-signing parties](https://en.wikipedia.org/wiki/Key_signing_party).

It's a great way to meet new people and get started with personal cryptography. PGP is how investigative journalists can securely communicate with inside sources and whistle-blowers, however, this is not just for those who need it for their safety—it's also a useful thing to have for authenticating commits in open source projects.


### Joining the Party

The party will be on Friday the 9th March at 15:35 in Hallway. To get involved you must submit your key beforehand.

To do so, just create a YAML file in the `keys` directory. The filename should match your GitHub username.

```yaml
# /keys/[username].yaml
name: <your name as on your ID and PGP identity>
fingerprint: <your PGP fingerprint>
```

Tips:

 - Your name must match the name in your ID (where possible).
 - Your name must match the name in your PGP Identity (if you don't know what this means don't worry, we can help you on the day).
 - Use your key _fingerprint_, not the key ID. The fingerprint is 40 characters long, but might have spaces or start with `0x`.


### Event Format

For those in-the-know, we will be implementing the [Zimmermann–Sassaman key-signing protocol](https://en.wikipedia.org/wiki/Zimmermann%E2%80%93Sassaman_key-signing_protocol#Sassaman-Efficient).

If you do not already have a PGP key, and would like to get started with personal cryptography, please come along with your devices and we will help you get setup. Alongside this, there will also be time for verifying other types of digital identities e.g. those used by WhatsApp/Signal/Telegram etc.


### Before the Event

In order to verify everyone efficiently, we ask for participants to try to generate their keys before the big day (see details below) and submit these either as pull request to https://github.com/pyconsk/2018.pycon.sk/tree/master/openpgp-key-signing-party or email them to info+pgp@pycon.sk. If you have any issues doing this, we can help you on the day.

### What to bring?

* **Government issued ID**—Please note, for those with existing keys, that your ID should, if possible, exactly match the identity used on the PGP key you wish to have verified e.g. if your key says Lizzy but your ID says Elizabeth, you will need to add a new identity to your key. If you do not know how to do this we can help you. If this is not possible (your chosen name and legal name differ, or you do not posses such ID), don't worry you can still participate, but signing parties may choose to assign a lower validity rating to your key.

* If you do not have a PGP key, please come with a device with an OpenPGP implementation installed (please see Install below) and we will talk you through how to get started. This does not need to be a laptop - there are available implementations for iOS and Android devices also.

### Install

Install an OpenPGP implementation:

* Mac: https://gpgtools.org/ `brew cask install gpgtools`
* Windows: https://www.gpg4win.org/ `choco install gpg4win`
* Linux (desktop): Should be already installed. You might need to upgrade
  to a package called `gnupg2`
* Android: https://www.openkeychain.org/
* iOS: https://privacyapp.io/
