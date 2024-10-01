#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../src/converter.cpp" // Include the converter implementation

namespace py = pybind11;

PYBIND11_MODULE(Excel2CSV, m) {
    m.doc() = "A C++ library to convert XLSX files to CSV format";

    m.def("convert", &xlsx_to_csv, "Convert an XLSX file to CSV format",
          py::arg("file_path"));
}
