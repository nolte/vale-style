# Vale style

[![GitHub Project Stars](https://img.shields.io/github/stars/nolte/vale-style.svg?label=Stars&style=social)](https://GitHub.com/nolte/vale-style) [![GitHub Issue Tracking](https://img.shields.io/github/issues-raw/nolte/vale-style.svg)](https://GitHub.com/nolte/vale-style) [![GitHub LatestRelease](https://img.shields.io/github/release/nolte/vale-style.svg)](https://GitHub.com/nolte/vale-style) [![.github/workflows/build-static-tests.yaml](https://github.com/nolte/vale-style/actions/workflows/build-static-tests.yaml/badge.svg)](https://github.com/nolte/vale-style/actions/workflows/build-static-tests.yaml) [![.github/workflows/release-cd-deliver-docs.yml](https://github.com/nolte/vale-style/actions/workflows/release-cd-deliver-docs.yml/badge.svg)](https://github.com/nolte/vale-style/actions/workflows/release-cd-deliver-docs.yml)

---


<!--intro-start-->
[Vale](https://github.com/errata-ai/vale) Package, for share spelling style and vocabularies between different Projects.
<!--intro-end-->


## Develop

```
mkdir -p ./build/nolte-style
cp -R src/* ./build/nolte-style/
cd ./build/
zip -r nolte-style.zip nolte-style
rm -rf ./build
```

will be create a archive like

```sh
.
├── nolte-style
│   └── styles
│       ├── config
│       │   └── vocabularies
│       │       └── technical
│       │           └── accept.txt
│       └── nolte-style
│           └── .keep
└── tree.txt

6 directories, 3 files
```


## Usage

Add the Latest release as Package Dependency

```
...

Packages =  https://github.com/nolte/vale-style/releases/download/v0.1.0/nolte-styles.zip


Vocab = "technical"

[*.md]
BasedOnStyles =  Vale

```

```
vale sync
```

```
vale .
```
