import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles, useTheme } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableFooter from '@mui/material/TableFooter';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import IconButton from '@mui/material/IconButton';
import FirstPageIcon from '@mui/icons-material/FirstPage';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import LastPageIcon from '@mui/icons-material/LastPage';
import defaultAvatar from "../../assets/images/users/default_avatar.jpg";
import TableHead from '@mui/material/TableHead';
import timer from '../../assets/icons/timer.svg';
import HSBar from "react-horizontal-stacked-bar-chart";
import RenderAsyncUserAvatar from "../Avatars/UserAvatar";


const useStyles1 = makeStyles((theme) => ({
    root: {
        flexShrink: 0,
        marginLeft: theme.spacing(2.5),
    },
}));

function TablePaginationActions(props) {
    const classes = useStyles1();
    const theme = useTheme();
    const { count, page, rowsPerPage, onChangePage } = props;

    const handleFirstPageButtonClick = (event) => {
        onChangePage(event, 0);
    };

    const handleBackButtonClick = (event) => {
        onChangePage(event, page - 1);
    };

    const handleNextButtonClick = (event) => {
        onChangePage(event, page + 1);
    };

    const handleLastPageButtonClick = (event) => {
        onChangePage(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1));
    };

    return (
        <div className={classes.root}>
            <IconButton
                onClick={handleFirstPageButtonClick}
                disabled={page === 0}
                aria-label="first page"
            >
                {theme.direction === 'rtl' ? <LastPageIcon /> : <FirstPageIcon />}
            </IconButton>
            <IconButton onClick={handleBackButtonClick} disabled={page === 0} aria-label="previous page">
                {theme.direction === 'rtl' ? <KeyboardArrowRight /> : <KeyboardArrowLeft />}
            </IconButton>
            <IconButton
                onClick={handleNextButtonClick}
                disabled={page >= Math.ceil(count / rowsPerPage) - 1}
                aria-label="next page"
            >
                {theme.direction === 'rtl' ? <KeyboardArrowLeft /> : <KeyboardArrowRight />}
            </IconButton>
            <IconButton
                onClick={handleLastPageButtonClick}
                disabled={page >= Math.ceil(count / rowsPerPage) - 1}
                aria-label="last page"
            >
                {theme.direction === 'rtl' ? <FirstPageIcon /> : <LastPageIcon />}
            </IconButton>
        </div>
    );
}

TablePaginationActions.propTypes = {
    count: PropTypes.number.isRequired,
    onChangePage: PropTypes.func.isRequired,
    page: PropTypes.number.isRequired,
    rowsPerPage: PropTypes.number.isRequired,
};

/*function createData(name, calories, fat) {
    return { name, calories, fat };
}*/

/*const rows = [
    createData('Cupcake', 305, 3.7),
    createData('Donut', 452, 25.0),
    createData('Eclair', 262, 16.0),
    createData('Frozen yoghurt', 159, 6.0),
    createData('Gingerbread', 356, 16.0),
    createData('Honeycomb', 408, 3.2),
    createData('Ice cream sandwich', 237, 9.0),
    createData('Jelly Bean', 375, 0.0),
    createData('KitKat', 518, 26.0),
    createData('Lollipop', 392, 0.2),
    createData('Marshmallow', 318, 0),
    createData('Nougat', 360, 19.0),
    createData('Oreo', 437, 18.0),
].sort((a, b) => (a.calories < b.calories ? -1 : 1));*/

const useStyles2 = makeStyles({
    table: {
        minWidth: 500,
    },
});

export default function TableDashboard(props) {

    const classes = useStyles2();
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(5);

    const emptyRows = rowsPerPage - Math.min(rowsPerPage, props.contacts.length - page * rowsPerPage);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    return (
        <Table className={classes.table} aria-label="custom pagination table">
            <TableHead>
                <TableRow>
                    <TableCell align="left" style={{width:"40%",fontWeight:600}}><img src={timer} style={{width:20}}/> <text>Employés ({props.contacts.length})</text></TableCell>
                    <TableCell align="center" style={{width:"40%",fontWeight:600}}>Heures totales</TableCell>
                    <TableCell align="center" style={{width:"10%",fontWeight:600}}>Capacité</TableCell>
                    <TableCell align="center" style={{width:"10%",fontWeight:600}}>Heures facturables</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {(rowsPerPage > 0 ? props.contacts.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage) : props.contacts).map((row,key) => (
                    <TableRow key={key}>
                        <TableCell component="th" scope="row" style={{width:"25%"}}>
                            <RenderAsyncUserAvatar email={row.user.email} />
                            {/*<div className="media align-items-center">
                                <img
                                    className=" rounded-circle text-center"
                                    style={{
                                        width: 60,
                                        height: 60,
                                        objectFit: "cover"
                                    }}
                                    src={row.imageUrl || defaultAvatar}
                                    alt=""/>

                                <div className="ml-1"
                                     style={{
                                         color: "#000",
                                         fontFamily: "sans-serif",
                                         fontWeight: 600,
                                         fontSize: 12
                                     }}>{row.user.nom} {row.user.prenom}
                                </div>
                            </div>*/}
                        </TableCell>
                        <TableCell style={{ width: "40%" }} align="center">
                            <div className="row w-100">
                                <text>20.00</text>
                                <HSBar
                                    showTextDown
                                    id="hsbarExample"
                                    outlineWidth={0.2}
                                    outlineRadius={10}
                                    outlineColor="#a6a6a6"
                                    data={[
                                        { value: 60,description: "0%", color: "#1998ed" },
                                        { value: 20, description: "60%", color: "#a5d6fa" },
                                        { value: 20, description: "80%", color: "white"}
                                    ]}
                                />
                            </div>


                        </TableCell>
                        <TableCell style={{ width: "10%" }} align="center">

                        </TableCell>
                        <TableCell style={{ width: "10%" }} align="center">
                            {row.duree}
                        </TableCell>
                    </TableRow>
                ))}

                {emptyRows > 0 && (
                    <TableRow style={{ height: 53 * emptyRows }}>
                        <TableCell colSpan={6} />
                    </TableRow>
                )}
            </TableBody>
            <TableFooter>
                <TableRow>
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 25, { label: 'All', value: -1 }]}
                        colSpan={3}
                        count={props.contacts.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        SelectProps={{
                            inputProps: { 'aria-label': 'rows per page' },
                            native: true,
                        }}
                        onChangePage={handleChangePage}
                        onChangeRowsPerPage={handleChangeRowsPerPage}
                        ActionsComponent={TablePaginationActions}
                        labelRowsPerPage="Lignes par page"
                    />
                </TableRow>
            </TableFooter>
        </Table>
    );
}
