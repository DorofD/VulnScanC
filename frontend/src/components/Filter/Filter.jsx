import React from "react";
import FilterIcon from '../../svg_images/Filter.svg';
import "./Filter.css"
/**
 * Компонент фильтрации логов.
 *
 * @param {Object} props
 * @param {React.ReactNode} props.children - Элементы фильтра: input и select, например:
 * 
 * <input type="text" className="filter" placeholder="Текст записи" onChange={e => setFilterLogs({ ...filterLogs, note: e.target.value })} value={filterLogs.note} />
 * 
 * @param {React.ReactNode} props.onClick - функция очистки фильтра, например:
 * onClick={() => setFilterLogs({ datetime: '', status: '', note: '' })}
 * 
 * 
 */
export default function Filter({ children, onClick, closeText = 'Очистить' }) {

    return (
        <div className="filterContainer">
            <FilterIcon
                className="filterIconStyle"
            />
            {children}
            <button onClick={onClick}>{closeText}</button>
        </div>
    );
}
