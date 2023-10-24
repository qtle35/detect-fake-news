import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Table, Button } from "react-bootstrap";

function Maus() {
    const [maus, setMaus] = useState([]);
    const navigate = useNavigate();
    // const [searchTerm, setSearchTerm] = useState("");

    const onViewClick = (id) => {
        navigate(`/mau/${id}`);
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/maus/delete/${id}`);
            fetchMaus();
        } catch (error) {
            console.error("Error deleting mau:", error);
        }
    };

    const fetchMaus = async () => {
        try {
            const response = await axios.get('http://localhost:5000/maus');
            setMaus(response.data);
        } catch (error) {
            console.error("Error fetching maus:", error);
        }
    };

    useEffect(() => {
        fetchMaus();
    }, []);

    return (
        <div>
            <h2 className="text-center">Mau List</h2>
            <div className="row">
                <div className="col">
                    <button className="btn btn-primary" onClick={() => onViewClick(-1)}>
                        Thêm Mẫu
                    </button>
                    <Table striped bordered hover>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Tiêu đề</th>
                                <th>Nội dung</th>
                                <th>Thể loại</th>
                                <th>Ngày tạo mẫu</th>
                                <th>Ngày sửa mẫu</th>
                                <th>Tên Nhãn</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {maus.map((mau) => (
                                <tr key={mau.id}>
                                    <td>{mau.id}</td>
                                    <td>{mau.title}</td>
                                    <td>{mau.noiDung}</td>
                                    <td>{mau.theLoai}</td>
                                    <td>{new Date(mau.ngayTaoMau).toLocaleDateString()}</td>
                                    <td>
                                        {mau.ngaySuaMau !== '01-01-1970' ? new Date(mau.ngaySuaMau).toLocaleDateString() : ''}
                                    </td>
                                    <td>{mau.nhan_name}</td> {/* Tên nhãn từ bảng "nhan" */}
                                    <td>
                                        <Button
                                            variant="primary"
                                            className="me-2"
                                            onClick={() => onViewClick(mau.id)}
                                        >
                                            View
                                        </Button>
                                        <Button
                                            variant="danger"
                                            onClick={() => handleDelete(mau.id)}
                                        >
                                            Delete
                                        </Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                </div>
            </div>
        </div>
    );
}

export default Maus;
