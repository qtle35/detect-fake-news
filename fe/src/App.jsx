import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import CustomSidebar from './components/sidebar';

function App() {
  return (
    <BrowserRouter>
      <div className='grid grid-cols-6'>
        <div className='col-span-1'>
          <CustomSidebar />
        </div>
        <div className='col-span-5'>
          <main>
            <Routes>
              <Route path="/home" element={<Home />} />
            </Routes>
          </main>
        </div>

      </div>
    </BrowserRouter>
  );
}

export default App;
