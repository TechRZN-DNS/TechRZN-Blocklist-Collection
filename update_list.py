name: Daily Blocklist Update

on:
  schedule:
    - cron: '0 0 * * *' # Täglich um Mitternacht
  workflow_dispatch: # Ermöglicht manuelles Starten

permissions:
  contents: write # WICHTIG: Erlaubt dem Bot, die Listen zu speichern

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4 # Update auf v4 (behebt die Warnung)

      - name: Set up Python
        uses: actions/setup-python@v5 # Update auf v5 (behebt die Warnung)
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install requests

      - name: Run Update Script
        run: python update_list.py

      - name: Commit and Push changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add combined_blocklist.txt lists/*.txt whitelist.txt
          git commit -m "Update blocklists [$(date +'%Y-%m-%d')]" || exit 0
          git push
