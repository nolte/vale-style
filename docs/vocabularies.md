# Vocabularies

The package ships two vocabularies. Consumers opt in via the `Vocab` directive in their own `.vale.ini`:

```ini
Vocab = technical, esphome
```

Vale loads each listed group from `styles/config/vocabularies/<name>/accept.txt` inside the unpacked package.

## `technical`

General-purpose terminology that shows up across mixed-stack projects — Ansible, ESPHome, mkdocs, Taskfile, zsh, and similar tool names; plus a handful of words that plain English dictionaries flag as typos (`dotfile`, `untrusted`, `env`).

Use this as the default vocabulary for most repos.

## `esphome`

ESPHome-specific terms: hardware identifiers (`ESP8285`, `HLW8012`, `SP111`), GPIO pin names (`GPIO00`–`GPIO15`), YAML config keys (`baud_rate`, `status_led`, `restore_mode`, `restore_from_flash`, `early_pin_init`, `turn_on_action`, `turn_off_action`), and related domain words (`automations`, `Datetime`, `dBm`).

Activate it additionally to `technical` when your docs cover ESPHome device configuration.

## How entries are matched

Each line in `accept.txt` is a **regex**, not a literal string. This is a Vale convention — take advantage of it to collapse related forms into one entry instead of listing every variant.

| Entry | Matches |
| --- | --- |
| `ESPHome` | `ESPHome` |
| `[Pp]robot` | `probot`, `Probot` |
| `[hH]ostnames?` | `hostname`, `hostnames`, `Hostname`, `Hostnames` |
| `LEDs?` | `LED`, `LEDs` |

Keep entries **case-sensitive by default**: write `[Pp]robot` rather than `(?i)probot`, so the vocabulary still flags unintended lowercase variants in places where only the proper-noun form is correct.
