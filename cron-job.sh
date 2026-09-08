#!/bin/sh
set -eu
cd "$(dirname "$0")"
node -e "require('dotenv').config(); const {openDatabase}=require('./database'); require('./scraper').runScraper(openDatabase()).then(console.log)"
