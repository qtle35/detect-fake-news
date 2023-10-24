import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";

function MauDetail() {
    const { id } = useParams();
    const [mau, setMau] = useState({});
    const [isEditing, setIsEditing] = useState(id === "-1");
    const [labels, setLabels] = useState([]);
    const [selectedLabel, setSelectedLabel] = useState("true");

    useEffect(() => {
        const fetchMau = async () => {
            try {
                if (id !== "-1") {
                    const response = await axios.get(`http://localhost:5000/maus/${id}`);
                    const data = response.data;

                    const formattedNgayTaoMau = formatDate(data.ngayTaoMau);
                    const formattedNgaySuaMau = formatDate(data.ngaySuaMau);
                    setMau({ ...data, ngayTaoMau: formattedNgayTaoMau, ngaySuaMau: formattedNgaySuaMau });
                }
            } catch (error) {
                console.log(error);
            }
        };
        fetchMau();
        fetchLabels();
    }, [id]);

    const fetchLabels = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/label`);
            setLabels(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const formatDate = (inputDate) => {
        const date = new Date(inputDate);
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, "0");
        const day = date.getDate().toString().padStart(2, "0");
        return `${year}-${month}-${day}`;
    };

    const handleEdit = () => {
        setIsEditing(true);
    };

    const handleSave = async () => {
        if (id === "-1") {
            await axios.post('http://localhost:5000/maus/save', {
                ...mau,
                nhan_id: parseInt(selectedLabel)
            });
            console.log("Mau created successfully.");
        } else {
            await axios.put(`http://localhost:5000/maus/update/${id}`, {
                ...mau,
                nhan_id: parseInt(selectedLabel)
            });
            console.log("Mau updated successfully.");
        }
        setIsEditing(false);
    };

    return (
        <div className="container">
            <h1 className="mb-4">{id === "-1" ? "New Mau" : `Mau ${id}`}</h1>
            <div className="mb-2">
                <Link to="/maus">Quay lại</Link>
            </div>
            <form onSubmit={handleSave}>
                <div className="row">
                    <div className="col-lg-6">
                        <div className="row mb-3">
                            <div className="col">
                                <label className="form-label required">Tiêu đề:</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={mau.title || ""}
                                    disabled={!isEditing}
                                    onChange={(e) => setMau({ ...mau, title: e.target.value })}
                                />
                            </div>
                            <div className="col">
                                <label className="form-label required">Thể loại:</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    value={mau.theLoai || ""}
                                    disabled={!isEditing}
                                    onChange={(e) => setMau({ ...mau, theLoai: e.target.value })}
                                />
                            </div>
                        </div>
                        <div className="col">
                            <label className="form-label required">Nội dung:</label>
                            <textarea
                                className="form-control"
                                value={mau.noiDung || ""}
                                disabled={!isEditing}
                                onChange={(e) => setMau({ ...mau, noiDung: e.target.value })}
                            />
                        </div>
                        <hr />
                        <div className="row mb-3">
                            <div className="col">
                                <label className="form-label required">Ngày tạo mẫu:</label>
                                <input
                                    type="date"
                                    className="form-control"
                                    value={mau.ngayTaoMau || ""}
                                    disabled={!isEditing}
                                    onChange={(e) => setMau({ ...mau, ngayTaoMau: e.target.value })}
                                />
                            </div>
                            <div className="col">
                                <label className="form-label required">Ngày sửa mẫu:</label>
                                <input
                                    type="date"
                                    className="form-control"
                                    value={mau.ngaySuaMau && mau.ngaySuaMau !== '1970-01-01' ? formatDate(mau.ngaySuaMau) : ""}
                                    disabled={!isEditing}
                                    onChange={(e) => setMau({ ...mau, ngaySuaMau: e.target.value })}
                                />
                            </div>
                        </div>
                        <div className="mb-3">
                            <label className="form-label required">Nhãn:</label>
                            <select
                                className="border-1 form-select"
                                onChange={(e) => setSelectedLabel(e.target.value)}
                                disabled={!isEditing}
                                value={id === "-1" ? selectedLabel : mau.nhan_id}
                            >
                                <option disabled value="default">Chọn nhãn</option>
                                {labels.map((label) => (
                                    <option key={label.id} value={label.id}>
                                        {label.name}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <hr />
                    </div>
                </div>
                <div className="row mt-5" style={{ borderTop: "2px solid" }}>
                    <div className="col"></div>
                    <div className="col"></div>
                    <div className="col mt-1">
                        {id === "-1" ? (
                            <button className="btn btn-primary" type="button" disabled={!isEditing} onClick={handleSave}>
                                Add
                            </button>
                        ) : isEditing ? (
                            <button className="btn btn-primary" type="button" onClick={handleSave} disabled={!isEditing}>
                                Save
                            </button>
                        ) : (
                            <button className="btn btn-primary" type="button" onClick={handleEdit}>
                                Edit
                            </button>
                        )}
                    </div>
                </div>
            </form>
        </div>
    );
}

export default MauDetail;
