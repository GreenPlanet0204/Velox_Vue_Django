import axios from "axios";
import {mergeWith} from "lodash/object";
import {isArray} from "lodash/lang";

function getArrayVal(arr, keyVal) {
  let obj = arr.find(o => o.value === keyVal);
  return obj.text;
}


function ExecuteRequest(url, data = []) {

  return axios.get(url).then(response => {
    const resp = response.data;
    const results = resp.results;
    for (const item of results) {
      data.push(item);
    }
    if (resp.next == null) return data
    return ExecuteRequest(resp.next, data);

  });

}

export {
  getArrayVal,
  ExecuteRequest
};
