import pytest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
from mma_stats.scrappers.ufc_athletes_scrapper import UFCScraper
from mma_stats.constants import SELECTORS

@pytest.fixture
def sample_athlete_html():
    return """
    <div class="c-listing-athlete-flipcard__inner">
        <a href="/athlete/john-doe-123" class="e-button--black"></a>
        <span class="c-listing-athlete__name">John Doe</span>
        <span class="c-listing-athlete__nickname">The Fighter</span>
        <span class="c-listing-athlete__record">10-2-1 (V-D-E)</span>
        <div class="field--name-stats-weight-class">
            <div class="field__item">Lightweight</div>
        </div>
    </div>
    """

@pytest.fixture
def mock_scraper():
    return UFCScraper()

def test_parse_record():
    scraper = UFCScraper()
    result = scraper._parse_record("10-2-1 (V-D-E)")
    assert tuple(result) == ("10", "2", "1")
    assert tuple(scraper._parse_record("N/A")) == ("N/A", "N/A", "N/A")

def test_process_athlete(mock_scraper, sample_athlete_html):
    with patch.object(mock_scraper, 'scrape_athlete_profile', return_value={}):
        soup = BeautifulSoup(sample_athlete_html, 'html.parser')
        athlete_element = soup.find("div", class_="c-listing-athlete-flipcard__inner")
        
        # Debug prints to help identify the issue
        print("HTML:", athlete_element.prettify())
        print("Name found:", mock_scraper._get_text(athlete_element, SELECTORS['name']))
        print("Nickname found:", mock_scraper._get_text(athlete_element, SELECTORS['nickname']))
        print("Record found:", mock_scraper._get_text(athlete_element, SELECTORS['record']))
        print("Weight Class found:", mock_scraper._get_text(athlete_element, SELECTORS['weight_class']))
        
        result = mock_scraper._process_athlete(athlete_element)
        
        assert result["Name"] == "John Doe"
        assert result["Nickname"] == "The Fighter"
        assert result["Wins"] == "10"
        assert result["Losses"] == "2"
        assert result["Draws"] == "1"
        assert result["Weight Class"] == "Lightweight"

@pytest.mark.vcr
def test_scrape_all_athletes(mock_scraper):
    with patch.object(mock_scraper, 'scrape_athletes_from_page') as mock_scrape:
        mock_scrape.return_value = [
            {
                "Athlete ID": "123",
                "Name": "John Doe",
                "Nickname": "The Fighter",
                "Wins": "10",
                "Losses": "2",
                "Draws": "1",
                "Weight Class": "Lightweight"
            }
        ]
        
        athletes = mock_scraper.scrape_all_athletes()
        assert len(athletes) > 0
        assert athletes[0].name == "John Doe"

def test_get_text():
    """Test the _get_text method specifically"""
    scraper = UFCScraper()
    html = """
    <div>
        <span class="c-listing-athlete__name">John Doe</span>
        <span class="c-listing-athlete__nickname">The Fighter</span>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')
    assert scraper._get_text(soup, 'span.c-listing-athlete__name') == "John Doe"
    assert scraper._get_text(soup, 'span.c-listing-athlete__nickname') == "The Fighter"
    assert scraper._get_text(soup, 'span.nonexistent') == "N/A" 