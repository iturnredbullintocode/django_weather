


/**
// only usable when not manually importing entire react library, but compiling via node
import { createRoot } from 'react-dom/client';

function NavigationBar() {
  // TODO: Actually implement a navigation bar
  return <h1>test123</h1>;
}

const domNode = document.getElementById('test_item_1');
const root = createRoot(domNode);
root.render(<NavigationBar />);
**/

function MyApp() {
    return <h1>testing display capabilities</h1>;
  }

  const container = document.getElementById('test_item_1');
  const root = ReactDOM.createRoot(container);
  root.render(<MyApp />);




const getMessage = () => "testing display capabilities 2";
document.getElementById('test_item_2').innerHTML = getMessage();