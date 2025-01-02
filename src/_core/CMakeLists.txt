set(PYBIND11_FINDPYTHON ON)

find_package(pybind11 CONFIG REQUIRED)

set(target_name _core)

file(GLOB_RECURSE internal_srcs "src/*.cpp")
file(GLOB_RECURSE internal_hdrs "include/*.hpp")

generate_git_header(VERSION_NAMESPACE_PREFIX _core)

pybind11_add_module(${target_name} MODULE ${internal_srcs} ${internal_hdrs})
warn_target(${target_name})
harden_target(${target_name})
sanitize_target(${target_name})

target_include_interface_directories(
  ${target_name} ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${CMAKE_CURRENT_BINARY_DIR}/git_version)

target_link_libraries(${target_name} PRIVATE ${target_name_internal})

install(TARGETS ${target_name} DESTINATION ${CMAKE_PROJECT_NAME})

install_dependency(TARGETS ${target_name} DEPENDS_DESTINATION
                   ${CMAKE_PROJECT_NAME})
