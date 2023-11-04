import { useEffect, useState } from "react";
import axios from 'axios';
import { FixedSizeList as List } from 'react-window';
import { Table, Button } from "react-bootstrap";
import "./style.css"

function SelectSamples(props) {
    const [samples, setSamples] = useState([]);
    const [selected, setSelected] = useState([]);
    const [expandedMaus, setExpandedMaus] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        axios.get('http://localhost:5000/getsamples')
            .then((response) => {
                setSamples(response.data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }, []);

    const handleRowSelect = (mau) => {
        const newSelected = [...selected];
        const index = newSelected.findIndex(s => s.id === mau.id);
        if (index === -1) {
            newSelected.push(mau);
        } else {
            newSelected.splice(index, 1);
        }
        setSelected(newSelected);
        console.log(selected)
    };

    const handleSelectAll = () => {
        if (selected.length === samples.length) {
            setSelected([]);
        } else {
            setSelected([...samples]);
        }
    };

    const toggleExpand = (id) => {
        if (expandedMaus.includes(id)) {
            setExpandedMaus(expandedMaus.filter((mauId) => mauId !== id));
        } else {
            setExpandedMaus([...expandedMaus, id]);
        }
    };
    const handleRetrainSubmit = () => {
        setLoading(true);
        axios.post('http://localhost:5000/retrain', selected)
            .then((response) => {
                setLoading(false);
                window.location.reload();
            })
            .catch((error) => {
                console.error('Error:', error);
                setLoading(false);
                alert('Retraining failed. Please try again.');

            });
    };
    const RenderRow = ({ index, style }) => {
        const mau = samples[index];
        return (
            <div style={style}>
                <Table striped bordered hover aria-label="Sample Table">
                    <tbody>
                        <tr key={mau.id}>
                            <td style={{ width: '2%' }}>
                                <input
                                    type="checkbox"
                                    onChange={() => handleRowSelect(mau)}
                                    checked={selected.some(s => s.id === mau.id)}
                                />
                            </td >
                            <td style={{ width: '5%' }}>{mau.id}</td>
                            <td style={{ width: '15%' }}>{mau.title}</td>
                            <td>
                                {expandedMaus.includes(mau.id) ? mau.noiDung : `${mau.noiDung.slice(0, 200)}...`}
                                <span onClick={() => toggleExpand(mau.id)} className="expand-icon">
                                    {expandedMaus.includes(mau.id) ? "-" : "+"}
                                </span>
                            </td>
                            <td style={{ width: '7%' }}>{mau.theLoai}</td>
                            <td style={{ width: '8%' }}>{mau.ngayTaoMau}</td>
                            <td style={{ width: '8%' }}>{mau.ngaySuaMau || ""}</td>
                            <td style={{ width: '5%' }}>{mau.nhan_name}</td>
                        </tr>
                    </tbody>
                </Table>
            </div>
        );
    };

    // Render header row (column titles) outside the Row function to prevent duplication
    const HeaderRow = () => (
        <div>

            <h2 className="text-center">
                <Button variant="primary" className="custom-button" disabled={loading} onClick={() => handleRetrainSubmit('retrain')}>
                    Retrain
                    {loading && <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>}
                </Button>
                Chọn Mẫu
            </h2>
            <p>{selected.length}/{samples.length}</p>
            <Table striped bordered hover aria-label="Sample Table">
            <thead>
                <tr>
                    <th style={{ width: '2%' }}>
                        <input
                            type="checkbox"
                            onChange={handleSelectAll}
                            checked={selected.length === samples.length && samples.length !== 0}
                        />
                    </th>
                    <th style={{ width: '5%' }}>ID</th>
                    <th style={{ width: '15%' }}>Tiêu đề</th>
                    <th>Nội dung</th>
                    <th style={{ width: '7%' }}>Thể loại</th>
                    <th style={{ width: '8%' }}>Ngày tạo mẫu</th>
                    <th style={{ width: '8%' }}>Ngày sửa mẫu</th>
                    <th style={{ width: '5%' }}>Nhãn</th>
                </tr>
            </thead>
        </Table>
        </div >
        
    );

    return (
        <div>
            <HeaderRow />
            <List
                height={800}
                itemCount={samples.length}
                itemSize={75}
                width={"100%"}
            >
                {RenderRow}
            </List>
        </div>
    );
}

export default SelectSamples;
