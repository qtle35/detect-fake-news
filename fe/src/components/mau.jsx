import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Table, Button } from "react-bootstrap";
import ReactPaginate from "react-paginate";

function Maus() {
    const [maus, setMaus] = useState([]);
    const [currentPage, setCurrentPage] = useState(0);
    const [expandedMaus, setExpandedMaus] = useState([]);
    const mausPerPage = 10;
    const [searchTerm, setSearchTerm] = useState("");
    const [searchInput, setSearchInput] = useState(""); 
    const navigate = useNavigate();
    const [totalPages, setTotalPages] = useState(1);

    const onViewClick = (id) => {
        navigate(`/mau/${id}`);
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/maus/delete/${id}`);
            fetchMaus(currentPage, searchTerm);
        } catch (error) {
            console.error("Error deleting mau:", error);
        }
    };

    const fetchMaus = async (page = 1, perPage = 10, searchTerm = "") => {
        try {
            let apiUrl = `http://localhost:5000/maus?page=${page}&per_page=${perPage}`;
            if (searchTerm) {
                apiUrl = `http://localhost:5000/maus?title=${searchTerm}&page=${page}&per_page=${perPage}`;
            }

            const response = await axios.get(apiUrl);
            setMaus(response.data.maus);
            setTotalPages(Math.ceil(response.data.total_count / mausPerPage));
        } catch (error) {
            console.error("Error fetching maus:", error);
        }
    };

    useEffect(() => {
        fetchMaus(currentPage + 1, mausPerPage, searchTerm);
    }, [currentPage, searchTerm]);

    const handlePageClick = ({ selected }) => {
        setCurrentPage(selected);
    };

    const toggleExpand = (id) => {
        if (expandedMaus.includes(id)) {
            setExpandedMaus(expandedMaus.filter((mauId) => mauId !== id));
        } else {
            setExpandedMaus([...expandedMaus, id]);
        }
    };

    const searchMaus = () => {
        setSearchTerm(searchInput);
    };

    return (
        <div>
            <h2 className="text-center">Mẫu List</h2>
            <div className="row">
                <div className="col">
                    <div className="text-center mb-3">
                        <input
                            type="text"
                            placeholder="Search by Title"
                            value={searchInput} 
                            onChange={(e) => setSearchInput(e.target.value)}
                        />
                        <button className="btn btn-primary" onClick={searchMaus}>
                            Tìm Mẫu
                        </button>
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
                            {maus.map((mau) => (
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
                                    <td>{mau.ngayTaoMau}</td>
                                    <td>
                                        {mau.ngaySuaMau || ''}
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
                            pageCount={totalPages}
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
