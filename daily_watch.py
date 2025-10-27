name: Daily Logistics Watch

on:
  schedule:
    - cron: '0 2 * * *' # 02:00 UTC = 09:00 Asia/Bangkok
  workflow_dispatch: {}

jobs:
  run-watch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install feedparser requests python-dateutil pytz beautifulsoup4
      - name: Run script
        env:
          TZ: 'Asia/Bangkok'
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
          SMTP_HOST: ${{ secrets.SMTP_HOST }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASS: ${{ secrets.SMTP_PASS }}
          FROM_EMAIL: ${{ secrets.FROM_EMAIL }}
          TO_EMAIL: ${{ secrets.TO_EMAIL }}
        run: |
          python daily_watch.py
      - name: Upload CSV artifact
        uses: actions/upload-artifact@v4
        with:
          name: daily-logistics-csv
          path: daily_logistics_watch.csv
