import 'bootstrap/dist/css/bootstrap.min.css';
import Card from 'react-bootstrap/Card';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import {FaThList} from 'react-icons/fa';
import Button from 'react-bootstrap/Button';
import {useState, useRef, useEffect} from 'react';
import {GrCapacity} from 'react-icons/gr';
import Alert from 'react-bootstrap/Alert';

function App() {

  const [n_items, setNItems] = useState(0);
  const [capacity, setCapacity] = useState(0);
  const [table, setTable] = useState([]);
  const [gen_table_disabled, setGenTableDisabled] = useState(true);
  const [weights, setWeights] = useState([]);
  const [profits, setProfits] = useState([]);
  const [rec_dp1, setRecDp1] = useState(true);
  const [it_dp1, setItDp1] = useState(true);
  const [it_dp2, setItDp2] = useState(true);
  const [fetch_results, setFetchResults] = useState({});
  const bottomRef = useRef(null);
  const [errorFetch, setErrorFetch] = useState(false);

  const checkInputs = () => {
    let capacity = document.getElementById('capacity').value;
    if (capacity === '') {
      setRecDp1(true);
      setItDp1(true);
      setItDp2(true);
      return false;
    }
    
    for (let i = 0; i < n_items; i++) {
      let weight = document.getElementById('table_wp').rows[i+1].cells[1].children[0].value;
      let profit = document.getElementById('table_wp').rows[i+1].cells[2].children[0].value;
      if (weight === '' || profit === '') {
        setRecDp1(true);
        setItDp1(true);
        setItDp2(true);
        return false;
      }
    }

    setRecDp1(false);
    setItDp1(false);
    setItDp2(false);
  }

  const generateTable_wp = (n_items) => {
    let table = [];
    let header = [];
    header.push(<th>Item</th>);
    header.push(<th>Weight</th>);
    header.push(<th>Profit</th>);
    table.push(<tr>{header}</tr>);
    for (let i = 0; i < n_items; i++) {
      let children = [];
      children.push(<td>X{i+1}</td>);
      children.push(<td><Form.Control type='number' placeholder="Enter weight" onChange={() => {
        weights[i] = parseInt(document.getElementById('table_wp').rows[i+1].cells[1].children[0].value);
        checkInputs();
      }} /></td>);
      children.push(<td><Form.Control type='number' placeholder="Enter profit" onChange={() => {
        profits[i] = parseInt(document.getElementById('table_wp').rows[i+1].cells[2].children[0].value);
        checkInputs();
      }} /></td>);
      table.push(<tr>{children}</tr>);
    }
    return table;
  }

  function createTable(tableData) {
    let table = [];
    let children = [];
    let header = [];
    for (let i = 0; i < tableData.length; i++) {
      header.push(<th style={{textAlign: 'center'}}>{i}</th>);
    }
    table.push(<tr>{header}</tr>);
    for (let i = 0; i < tableData.length; i++) {
      children.push(<td>{tableData[i]}</td>);
    }
    table.push(<tr>{children}</tr>);
    return table;
  }

  function createTable_itdp1(tableData, index_colored) {
    let table = [];
    let header = [];
    header.push(<th style={{textAlign: 'center'}}>Item</th>);
    for (let i = 0; i < tableData[0].length; i++) {
      header.push(<th style={{textAlign: 'center'}}>{i}</th>);
    }
    table.push(<tr>{header}</tr>);
    for (let i = 0; i < tableData.length; i++) {
      let children = [];
      children.push(<td>X{i+1}</td>);
      for (let j = 0; j < tableData[i].length; j++) {
        if (j === index_colored[i]){
          children.push(<td style={{border: '2px solid red'}}>{tableData[i][j]}</td>);
        } else {
          children.push(<td>{tableData[i][j]}</td>);
        }
      }
      table.push(<tr>{children}</tr>);
    }

    return table;
  }

  function updateTable(method) {
    // Method 0: iteration + 1
    // Method 1: iteration - 1
    // Method 2: go to result
    if (method === 0) {
      setFetchResults({
        ...fetch_results,
        'iteration': fetch_results['iteration'] + 1,
        'it_matrix': fetch_results['it_matrix'] + 1,
        'table': createTable(fetch_results['memory'][fetch_results['it_matrix'] + 1])
      })
    } else if (method === 1) {
      setFetchResults({
        ...fetch_results,
        'iteration': fetch_results['iteration'] - 1,
        'it_matrix': fetch_results['it_matrix'] - 1,
        'table': createTable(fetch_results['memory'][fetch_results['it_matrix'] - 1])
      })
    } else {
      setFetchResults({
        ...fetch_results,
        'iteration': fetch_results['memory'].length,
        'it_matrix': fetch_results['memory'].length - 1,
        'table': createTable(fetch_results['memory'][fetch_results['memory'].length - 1])
      })
    }
  }

  const recursiveKnapsack = (capacity, weights, profits) => {
    fetch('http://localhost:8000/api/recursive_knapsack', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        capacity: parseInt(capacity),
        weights: weights,
        profits: profits
      })
    }).then(res => {
      if (res.ok) {
        return res.json()
      }
      return Promise.reject(res);
    })
    .then(data => {
      let memory = data['memory'];
      let z_star = data['z_star'];

      let json_data = {
        'algorithm': 'recursive_knapsack',
        'memory': memory,
        'table': createTable(memory[0]),
        'iteration': 1,
        'it_matrix': 0,
        'z_star': z_star,
        'pick': data['pick']
      }
      setFetchResults(json_data);
    })
    .catch(_ => {
      setErrorFetch(true);
      setRecDp1(true);
      setItDp1(true);
      setItDp2(true);
      setTimeout(() => {
        setErrorFetch(false);
        setRecDp1(false);
        setItDp1(false);
        setItDp2(false);
      }, 3000)
    });
  }

  const dinamic_knapsack_single_list = (capacity, weights, profits) => {
    fetch('http://localhost:8000/api/dinamic_knapsack_single_list', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        capacity: parseInt(capacity),
        weights: weights,
        profits: profits
      })
    }).then(res => {
      if (res.ok) {
        return res.json()
      }
      return Promise.reject(res);
    })
    .then(data => {
      let memory = data['memory'];
      let z_star = data['z_star'];

      let json_data = {
        'algorithm': 'dinamic_knapsack_single_list',
        'memory': memory,
        'table': createTable(memory[0]),
        'iteration': 1,
        'it_matrix': 0,
        'z_star': z_star,
        'pick': data['pick']
      }
      setFetchResults(json_data);
    })
    .catch(_ => {
      setErrorFetch(true);
      setRecDp1(true);
      setItDp1(true);
      setItDp2(true);
      setTimeout(() => {
        setErrorFetch(false);
        setRecDp1(false);
        setItDp1(false);
        setItDp2(false);
      }, 3000)
    });
  }

  const dinamic_knapsack_matrix = (capacity, weights, profits) => {
    fetch('http://localhost:8000/api/dinamic_knapsack_matrix', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        capacity: parseInt(capacity),
        weights: weights,
        profits: profits
      })
    }).then(res => {
      if (res.ok) {
        return res.json()
      }
      return Promise.reject(res);
    })
    .then(data => {
      // I create the resulting two tables from arrays received from the backend
      let a = data['a'];
      let z = data['z'];
      let z_star = data['z_star'];

      let index_colored = [parseInt(capacity)]
      for (let i = 1; i < a.length; i++) {
        if (a[i-1][index_colored[index_colored.length - 1]] === 1) {
          index_colored.push(index_colored[index_colored.length - 1] - weights[i-1]);
        } else {
          index_colored.push(index_colored[index_colored.length - 1]);
        }
      }

      let table_a = createTable_itdp1(a, index_colored);
      let table_z = createTable_itdp1(z.reverse(), index_colored);

      let json_data = {
        'algorithm': 'dinamic_knapsack_matrix',
        'table_a': table_a,
        'table_z': table_z,
        'z_star': z_star
      }
      setFetchResults(json_data);
    })
    .catch(_ => {
      setErrorFetch(true);
      setRecDp1(true);
      setItDp1(true);
      setItDp2(true);
      setTimeout(() => {
        setErrorFetch(false);
        setRecDp1(false);
        setItDp1(false);
        setItDp2(false);
      }, 3000)
    });
  }

  useEffect(() => {
    bottomRef.current?.scrollIntoView({behavior: 'smooth'});
  }, [fetch_results]);

  return (
    <div className="App">
        <h1 style={{justifyContent: 'center', color: 'white', display: 'flex', marginBottom: '50px'}}>0-1 Knapsack Problem - 3 Dynamic Programming Solutions</h1>
        <div style={{width: '60%', margin: '0 auto'}}>
          <Card>
            <Card.Body style={{display: 'flex', justifyContent: 'center', flexDirection: 'column'}}>
              <h1 style={{marginBottom: '30px'}}>0-1 KP Inputs</h1>
              <InputGroup className="mb-3">
                <InputGroup.Text id="basic-addon1"><GrCapacity /></InputGroup.Text>
                <Form.Control
                  id='capacity'
                  type='number'
                  placeholder="Enter capacity"
                  aria-label="capacity"
                  aria-describedby="basic-addon1"
                  onChange={(e) => {
                    setCapacity(e.target.value);
                    if (document.getElementById('table_wp')) {
                      checkInputs();
                    }
                  }}
                />
              </InputGroup>
              <InputGroup className="mb-3">
                <InputGroup.Text id="basic-addon1"><FaThList /></InputGroup.Text>
                <Form.Control
                  id='n_items'
                  type='number'
                  placeholder="Enter number of items"
                  aria-label="n_items"
                  aria-describedby="basic-addon1"
                  onChange={(e) => {
                    setNItems(e.target.value);
                    if (e.target.value === '' || e.target.value === 0) {
                      setGenTableDisabled(true);
                    }
                    if (e.target.value > 0) {
                      if (table.length === 0) {
                        setGenTableDisabled(false);
                      } else {
                        setGenTableDisabled(true);
                      }
                    }
                  }}
                />
            </InputGroup>
            <Button disabled={gen_table_disabled} variant="success" onClick={() => {
              let table = generateTable_wp(n_items);
              setTable(table);
              setGenTableDisabled(true);
            }}>Generate Table</Button>
            {table.length !== 0 && <div style={{marginTop: '30px'}}>
              <div className='scrollTable' style={{overflow: 'auto'}}>
                <table className="table table-bordered" id='table_wp'>
                  <tbody>
                    {table}
                  </tbody>
                </table>
              </div>
            </div>}
            {table.length !== 0 && 
              <>
                <div style={{display: 'flex', flexDirection: 'row', marginTop: '10px'}}>
                  {/* DP1 */}
                  <Button disabled={rec_dp1} style={{width: '33%', marginRight: '10px'}} variant="success" onClick={() => {
                    recursiveKnapsack(capacity, weights, profits);
                  }}>Recursion DP1</Button>
                  {/* dinamic_knackpack_matrix */}
                  <Button disabled={it_dp1} style={{width: '33%', marginRight: '10px'}} variant="success" onClick={() => {
                    dinamic_knapsack_matrix(capacity, weights, profits);
                  }}>Iterative DP1</Button>
                  {/* dinamic_knackpack_single_list */}
                  <Button disabled={it_dp2} style={{width: '33%'}} variant="success" onClick={() => {
                    dinamic_knapsack_single_list(capacity, weights, profits);
                  }}>Iterative DP2</Button>
                </div>
                <Button variant='success' style={{marginTop: '10px'}} onClick={() => {
                  setFetchResults({});
                  setCapacity(0);
                  setNItems(0);
                  setGenTableDisabled(true);
                  setTable([]);
                  setWeights([]);
                  setProfits([]);
                  document.getElementById('capacity').value = '';
                  document.getElementById('n_items').value = '';
                }}>Clear All</Button>
                <Alert variant={'danger'} style={{marginTop: '10px'}} show={errorFetch} >
                  There was an error fetching the results. Please change the weights and profits and try again.
                </Alert>
              </>
            }
            </Card.Body>
          </Card>
          {fetch_results['algorithm'] === 'dinamic_knapsack_matrix' &&
            <Card style={{marginBottom: '50px', marginTop: '50px'}}>
              <Card.Body style={{display: 'flex', justifyContent: 'center', flexDirection: 'column'}}>
                <div>
                  <h1 style={{marginBottom: '20px'}}>Result of Iterative DP1</h1>
                  <h3>Picks Table</h3>
                  <div className='scrollTable' style={{overflow: 'auto', marginBottom: '30px'}}>
                    <table className="table table-bordered">
                      <tbody>
                        {fetch_results['table_a']}
                      </tbody>
                    </table>
                  </div>
                  <h3>Values Table</h3>
                  <div className='scrollTable' style={{overflow: 'auto', marginBottom: '30px'}}>
                    <table className="table table-bordered">
                      <tbody>
                        {fetch_results['table_z']}
                      </tbody>
                    </table>
                  </div>
                  <h3>Z*: {fetch_results['z_star']}</h3>
                </div>
              </Card.Body>
            </Card>
          }
          {(fetch_results['algorithm'] === 'recursive_knapsack' || fetch_results['algorithm'] === 'dinamic_knapsack_single_list') &&
            <Card style={{marginBottom: '50px', marginTop: '50px'}}>
              <Card.Body style={{display: 'flex', justifyContent: 'center', flexDirection: 'column'}}>
                <div>
                  {fetch_results['algorithm'] === 'recursive_knapsack' && <h1 style={{marginBottom: '20px'}}>Result of Recursion DP1</h1>}
                  {fetch_results['algorithm'] === 'dinamic_knapsack_single_list' && <h1 style={{marginBottom: '20px'}}>Result of Iterative DP2</h1>}
                  <h3>Table - Iteration {fetch_results['iteration']}</h3>
                  <div className='scrollTable' style={{overflow: 'auto', marginBottom: '30px'}}>
                    <table className="table table-bordered">
                      <tbody>
                        {fetch_results['table']}
                      </tbody>
                    </table>
                  </div>
                  {fetch_results['iteration'] < fetch_results['memory'].length && 
                    <>
                      <Button variant="success" style={{marginRight: '10px'}} onClick={() => {
                          updateTable(0);
                        }}>Next Iteration</Button>
                      {fetch_results['iteration'] > 1 && <Button variant="success" style={{marginRight: '10px'}} onClick={() => {
                          updateTable(1);
                        }}>Previous Iteration</Button>}
                      <Button variant="success" onClick={() => {
                          updateTable(2);
                        }}>Go to result</Button>
                    </>
                  }
                  {fetch_results['iteration'] === fetch_results['memory'].length && 
                    <>
                      <Button variant="success" style={{marginBottom: '10px'}} onClick={() => {
                          updateTable(1);
                        }}>Previous Iteration</Button>
                      <h3>Z*: {fetch_results['z_star']}</h3>
                    </>
                  }
                  {fetch_results['iteration'] === fetch_results['memory'].length && 
                    fetch_results['pick'].map((item, index) => {
                        return <h3>X{index + 1} = {item}</h3>
                    })
                  }
                </div>
              </Card.Body>
            </Card>
          }
        </div>
        <div ref={bottomRef} />
      </div>
  );
}

export default App;
