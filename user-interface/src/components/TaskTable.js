import React from 'react'
import { useTable, useSortBy, useFilters, useGlobalFilter } from 'react-table'

function TaskTable({ columns, data }) {
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        state,
        setGlobalFilter
    } = useTable(
        {
            columns,
            data
        },
        useFilters,
        useGlobalFilter,
        useSortBy
    );

    const { globalFilter } = state;

    return (
        <div className="overflow-x-auto">
            <input
                className="p-2 mb-4 border border-gray-300 rounded-lg"
                placeholder="Search tasks..."
                value={globalFilter || ""}
                onChange={e => setGlobalFilter(e.target.value)}
            />

            <table {...getTableProps()} className="table-auto min-w-full bg-white border-collapse border border-gray-300">
                <thead>
                    {headerGroups.map(headerGroup => (
                        <tr {...headerGroup.getHeaderGroupProps()}>
                            {headerGroup.headers.map(column => (
                                <th
                                    {...column.getHeaderProps(column.getSortByToggleProps())}
                                    className="px-6 py-3 bg-gray-100 text-xs leading-4 text-gray-500 uppercase tracking-wider"
                                >
                                    {column.render("Header")}
                                    <span>
                                        {column.isSorted ? (column.isSortedDesc ? " 🔽" : " 🔼") : ""}
                                    </span>
                                </th>
                            ))}
                        </tr>
                    ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                    {rows.map(row => {
                        prepareRow(row);
                        return (
                            <tr {...row.getRowProps()}>
                                {row.cells.map(cell => (
                                    <td {...cell.getCellProps()} className="px-6 py-4 whitespace-no-wrap border-b border-gray-300">
                                        {typeof cell.value === "boolean" ? (cell.value ? "True" : "False") : cell.render("Cell")}
                                    </td>
                                ))}
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    )
}

export default TaskTable;
