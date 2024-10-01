#include <xlnt/xlnt.hpp>
#include <vector>
#include <string>
#include <sstream>

// Function to convert XLSX to CSV
std::vector<std::string> xlsx_to_csv(const std::string& file_path) {
    xlnt::workbook wb;
    wb.load(file_path);
    std::vector<std::string> csv_data;

    for (auto ws : wb) {
        std::stringstream ss;
        for (auto row : ws.rows(false)) {
            bool first = true;
            for (auto cell : row) {
                if (!first) {
                    ss << ",";
                }
                first = false;
                std::string cell_value = cell.to_string();
                // Handle commas and quotes in cell
                if (cell_value.find(',') != std::string::npos || cell_value.find('"') != std::string::npos) {
                    // Escape quotes
                    size_t pos = 0;
                    while ((pos = cell_value.find('"', pos)) != std::string::npos) {
                        cell_value.insert(pos, "\"");
                        pos += 2;
                    }
                    ss << "\"" << cell_value << "\"";
                } else {
                    ss << cell_value;
                }
            }
            ss << "\n";
        }
        csv_data.push_back(ss.str());
    }

    return csv_data;
}
