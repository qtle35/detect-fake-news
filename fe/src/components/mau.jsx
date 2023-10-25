import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Table, Button } from "react-bootstrap";
import ReactPaginate from "react-paginate";

function Maus() {
    const [maus, setMaus] = useState([]);
    const [expandedMaus, setExpandedMaus] = useState([]);
    const [currentPage, setCurrentPage] = useState(0);
    const mausPerPage = 5;
    const [searchTerm, setSearchTerm] = useState(""); // Step 1

    const navigate = useNavigate();

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

    const toggleExpand = (id) => {
        if (expandedMaus.includes(id)) {
            setExpandedMaus(expandedMaus.filter((mauId) => mauId !== id));
        } else {
            setExpandedMaus([...expandedMaus, id]);
        }
    };

    const pageCount = Math.ceil(maus.length / mausPerPage);

    const handlePageClick = ({ selected }) => {
        setCurrentPage(selected);
    };

    const filteredMaus = maus.filter((mau) => {
        return (
            mau.title.toLowerCase().includes(searchTerm.toLowerCase()) // Step 2
        );
    });

    const currentMaus = filteredMaus.slice(currentPage * mausPerPage, (currentPage + 1) * mausPerPage); // Step 4

    return (
        <div>
            <h2 className="text-center">Mẫu List</h2>
            <div className="row">

                <div className="col">
                    <div className="text-center mb-3">
                        <input
                            type="text"
                            placeholder="Search by Title"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)} // Step 3
                        />
                    </div>
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
                            {currentMaus.map((mau) => (
                                <tr key={mau.id}>
                                    <td>{mau.id}</td>
                                    <td>{mau.title}</td>
                                    <td>
                                        {expandedMaus.includes(mau.id) ? mau.noiDung : `${mau.noiDung.slice(0, 50)}...`}
                                        <button
                                            onClick={() => toggleExpand(mau.id)}
                                            className="btn btn-link"
                                        >
                                            {expandedMaus.includes(mau.id) ? "Ẩn" : "Hiện thêm"}
                                        </button>
                                    </td>
                                    <td>{mau.theLoai}</td>
                                    <td>{new Date(mau.ngayTaoMau).toLocaleDateString()}</td>
                                    <td>
                                        {mau.ngaySuaMau !== null ? new Date(mau.ngaySuaMau).toLocaleDateString() : ''}
                                    </td>
                                    <td>{mau.nhan_name}</td>
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
                    <div className="text-center">
                        <ReactPaginate
                            previousLabel={"Previous"}
                            nextLabel={"Next"}
                            breakLabel={"..."}
                            pageCount={pageCount}
                            marginPagesDisplayed={2}
                            pageRangeDisplayed={5}
                            onPageChange={handlePageClick}
                            containerClassName={"pagination"}
                            subContainerClassName={"pages pagination"}
                            activeClassName={"active"}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Maus;
