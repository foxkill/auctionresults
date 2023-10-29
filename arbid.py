import requests
import xml.etree.ElementTree as ET

def download_xml_file(cusip_number):
    """Downloads an XML file from TreasuryDirect.gov by a given CUSIP number.

    Args:
        cusip_number: The CUSIP number of the security to download the auction results for.

    Returns:
        The XML file as a string.
    """

    url = f"https://treasurydirect.gov/auctions/results/xml/{cusip_number}.xml"
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def calculate_percentage_primary_dealers_bought(xml_file):
    """Calculates the percentage of primary dealers bought.

    Args:
        xml_file: The XML file as a string.

    Returns:
        The percentage of primary dealers bought as a float.
    """

    xml_root = ET.fromstring(xml_file)

    primary_dealers_bought = float(xml_root.find("PrimaryDealers").find("AcceptedAmount").text)
    total_sold = float(xml_root.find("AllBidders").find("AcceptedAmount").text)

    percentage_primary_dealers_bought = (primary_dealers_bought / total_sold) * 100

    return percentage_primary_dealers_bought

def calculate_bid_to_cover_ratio(xml_file):
    """Calculates the bid-to-cover ratio.

    Args:
        xml_file: The XML file as a string.

    Returns:
        The bid-to-cover ratio as a float.
    """

    xml_root = ET.fromstring(xml_file)

    total_bids = float(xml_root.find("AllBidders").find("TotalBids").text)
    total_sold = float(xml_root.find("AllBidders").find("AcceptedAmount").text)

    bid_to_cover_ratio = total_bids / total_sold

    return bid_to_cover_ratio

def main():
    """Downloads the XML file for the given CUSIP number and calculates the percentage of primary dealers bought and the bid-to-cover ratio."""

    cusip_number = input("Enter the CUSIP number: ")

    xml_file = download_xml_file(cusip_number)

    percentage_primary_dealers_bought = calculate_percentage_primary_dealers_bought(xml_file)
    bid_to_cover_ratio = calculate_bid_to_cover_ratio(xml_file)

    print(f"Percentage of primary dealers bought: {percentage_primary_dealers_bought:.2f}%")
    print(f"Bid-to-cover ratio: {bid_to_cover_ratio:.2f}")

if __name__ == "__main__":
    main()
