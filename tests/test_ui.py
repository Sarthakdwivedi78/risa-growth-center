import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from streamlit.testing.v1 import AppTest
import pytest
import db

@pytest.mark.parametrize('page',['Overview','Growth Analytics','Campaign Management','Task Management','Experimentation','AI Growth Analyst','Data Management','Settings'])
def test_pages(page,tmp_path,monkeypatch):
    monkeypatch.setenv('RISA_DB',str(tmp_path/'ui.db'))
    at=AppTest.from_file(str(db.ROOT/'app.py'),default_timeout=45).run()
    at.sidebar.radio[0].set_value(page).run()
    assert not at.exception

def test_chat_confirmation(tmp_path,monkeypatch):
    monkeypatch.setenv('RISA_DB',str(tmp_path/'ui.db'))
    at=AppTest.from_file(str(db.ROOT/'app.py'),default_timeout=45).run()
    at.sidebar.radio[0].set_value('AI Growth Analyst').run()
    at.chat_input[0].set_value('Set C03 budget to INR 40000').run()
    assert not at.exception
    assert any(b.label=='Confirm and save' for b in at.button)
    next(b for b in at.button if b.label=='Confirm and save').click().run()
    at.chat_input[0].set_value('What is its budget?').run()
    assert not at.exception
    assert any('40,000' in m.value for m in at.markdown)

def test_empty_historical_filter(tmp_path,monkeypatch):
    from datetime import date
    monkeypatch.setenv('RISA_DB',str(tmp_path/'ui.db'))
    at=AppTest.from_file(str(db.ROOT/'app.py'),default_timeout=45).run()
    at.sidebar.date_input[0].set_value(date(2025,1,1)).run()
    assert not at.exception
    at.checkbox[0].set_value(True).run()
    assert not at.exception
