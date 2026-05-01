const API_URL = '/api';

const formListSection = document.getElementById('form-list-section');
const formDetailSection = document.getElementById('form-detail-section');
const successSection = document.getElementById('success-section');
const formList = document.getElementById('form-list');
const fieldsContainer = document.getElementById('fields-container');
const submissionForm = document.getElementById('submission-form');
const errorContainer = document.getElementById('error-container');

let currentFormId = null;

// Initial Load
async function init() {
    try {
        const response = await fetch(`${API_URL}/forms/active`);
        const forms = await response.json();
        
        formList.innerHTML = '';
        if (forms.length === 0) {
            formList.innerHTML = '<p>Không có form nào đang hoạt động.</p>';
            return;
        }

        forms.forEach(form => {
            const card = document.createElement('div');
            card.className = 'form-item';
            card.innerHTML = `
                <h4>${form.title}</h4>
                <p>${form.description || 'Không có mô tả'}</p>
            `;
            card.onclick = () => loadForm(form.id);
            formList.appendChild(card);
        });
    } catch (err) {
        formList.innerHTML = '<p class="error">Không thể tải dữ liệu API.</p>';
    }
}

async function loadForm(id) {
    currentFormId = id;
    try {
        const response = await fetch(`${API_URL}/forms/${id}`);
        const data = await response.json();
        
        document.getElementById('current-form-title').innerText = data.title;
        document.getElementById('current-form-desc').innerText = data.description || '';
        
        fieldsContainer.innerHTML = '';
        data.fields.forEach(field => {
            const group = document.createElement('div');
            group.className = 'field-group';
            
            let inputHtml = '';
            if (field.type === 'select') {
                inputHtml = `<select name="${field.id}" ${field.required ? 'required' : ''}>
                    <option value="">-- Chọn một tùy chọn --</option>
                    ${field.options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}
                </select>`;
            } else {
                const typeMap = {
                    'text': 'text',
                    'number': 'number',
                    'date': 'date',
                    'color': 'text' // Use text with regex check if needed, but 'color' input is better
                };
                const inputType = field.type === 'color' ? 'color' : typeMap[field.type];
                inputHtml = `<input type="${inputType}" name="${field.id}" ${field.required ? 'required' : ''} placeholder="${field.label}">`;
            }

            group.innerHTML = `
                <label>${field.label} ${field.required ? '<span style="color:#ef4444">*</span>' : ''}</label>
                ${inputHtml}
            `;
            fieldsContainer.appendChild(group);
        });

        formListSection.classList.add('hidden');
        formDetailSection.classList.remove('hidden');
    } catch (err) {
        alert('Lỗi khi tải chi tiết form');
    }
}

document.getElementById('back-btn').onclick = () => {
    formDetailSection.classList.add('hidden');
    formListSection.classList.remove('hidden');
    errorContainer.classList.add('hidden');
};

submissionForm.onsubmit = async (e) => {
    e.preventDefault();
    errorContainer.classList.add('hidden');
    
    const formData = new FormData(submissionForm);
    const values = [];
    
    for (let [fieldId, value] of formData.entries()) {
        values.push({ field_id: parseInt(fieldId), value: value });
    }

    try {
        const response = await fetch(`${API_URL}/forms/${currentFormId}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ values })
        });

        const result = await response.json();
        if (result.success) {
            formDetailSection.classList.add('hidden');
            successSection.classList.remove('hidden');
        } else {
            errorContainer.innerHTML = `<strong>Lỗi nhập liệu:</strong><br>${result.details.join('<br>')}`;
            errorContainer.classList.remove('hidden');
        }
    } catch (err) {
        alert('Lỗi hệ thống khi gửi form');
    }
};

init();
