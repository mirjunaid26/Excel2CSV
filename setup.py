import os
import sys
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11
from setuptools import find_packages

class CMakeBuild(build_ext):
    def run(self):
        # Ensure CMake is installed
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))
        
        for ext in self.extensions:
            self.build_extension(ext)
    
    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))
        
        cmake_args = [
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}',
            f'-DPYTHON_EXECUTABLE={sys.executable}'
        ]
        
        build_args = []
        
        cfg = 'Debug' if self.debug else 'Release'
        cmake_args += [f'-DCMAKE_BUILD_TYPE={cfg}']
        
        build_args += ['--config', cfg]
        
        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''),
            self.distribution.get_version())
        
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        
        subprocess.check_call(['cmake', os.path.abspath('.')] + cmake_args,
                              cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                              cwd=self.build_temp)
        
setup(
    name='Excel2CSV',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A C++ library to convert XLSX files to CSV format with Python bindings',
    long_description='',
    ext_modules=[Extension(
        'Excel2CSV',
        sources=['bindings/bindings.cpp'],
    )],
    cmdclass={'build_ext': CMakeBuild},
    zip_safe=False,
    install_requires=[
        'pybind11>=2.5.0',
        'xlnt'  # Ensure xlnt is available; alternatively, include it as a submodule or handle dependencies in CMake
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: C++',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    packages=find_packages(),
)
