use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn count_doubles_slice(val: &str) -> PyResult<u64> {
    let count = val.as_bytes().windows(2).filter(|slice| slice[0] == slice[1]).count();
    Ok(count as u64)
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn myrustpyo3(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(count_doubles_slice, m)?)?;
    Ok(())
}