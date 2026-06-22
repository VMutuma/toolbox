import csv
import json
import logging

def save_to_csv(data, filename):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Term", "Link", "Definition"])
            writer.writerows(data)
        logging.info(f"Data saved to '{filename}'.")
    except Exception as e:
        logging.error(f"Error while writing CSV file: {e}")
        raise

def csv_to_json(csv_filename, json_filename):
    try:
        data = []
        with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)

        with open(json_filename, mode="w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        logging.info(f"CSV converted to JSON! Data saved to '{json_filename}'.")
    except Exception as e:
        logging.error(f"Error while converting CSV to JSON: {e}")
        raise