#!/bin/bash

# Crea directory necessarie
mkdir -p ~/.streamlit
mkdir -p cache
mkdir -p cache/twelvedata
mkdir -p cache/yahoo

# Configura Streamlit
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
base = \"dark\"\n\
primaryColor = \"#f0b90b\"\n\
backgroundColor = \"#0A0A0F\"\n\
secondaryBackgroundColor = \"#1A1A24\"\n\
textColor = \"#ffffff\"\n\
" > ~/.streamlit/config.toml
