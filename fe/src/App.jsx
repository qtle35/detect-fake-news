import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import CustomSidebar from './components/sidebar';
import LabelPage from './components/label-page';
import React from 'react';
import LabelEdit from './components/label-edit';

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
              <Route path="/" element={<Home />} />
            </Routes>
          </main>
        </div>

      </div>
      {/* <Navbar /> */}
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/label' element={<LabelPage />} />
        <Route path='/label/:id' element={<LabelEdit />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
