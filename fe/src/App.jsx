import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import Maus from './components/mau';
import MauDetail from './components/mauDetail';
import CustomSidebar from './components/sidebar';
import LabelPage from './components/label-page';
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
              <Route path='/' element={<Home />} />
              <Route path='/label' element={<LabelPage />} />
              <Route path='/label/:id' element={<LabelEdit />} />
              <Route path='/maus' element={<Maus />} />
              <Route path='/mau/:id' element={<MauDetail />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
